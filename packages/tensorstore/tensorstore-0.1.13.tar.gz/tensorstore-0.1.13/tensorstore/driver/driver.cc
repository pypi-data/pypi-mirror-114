// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "tensorstore/driver/driver.h"

#include <ostream>

#include "tensorstore/driver/registry.h"
#include "tensorstore/index_space/alignment.h"
#include "tensorstore/index_space/json.h"
#include "tensorstore/index_space/transform_broadcastable_array.h"
#include "tensorstore/internal/arena.h"
#include "tensorstore/internal/data_type_json_binder.h"
#include "tensorstore/internal/lock_collection.h"
#include "tensorstore/internal/nditerable_copy.h"
#include "tensorstore/internal/nditerable_data_type_conversion.h"
#include "tensorstore/internal/nditerable_transformed_array.h"
#include "tensorstore/internal/no_destructor.h"

namespace tensorstore {
namespace internal {

namespace jb = tensorstore::internal_json_binding;

DriverRegistry& GetDriverRegistry() {
  static internal::NoDestructor<DriverRegistry> registry;
  return *registry;
}

Future<Driver::Handle> DriverSpec::Bound::Open(
    OpenTransactionPtr transaction, ReadWriteMode read_write_mode) const {
  return absl::UnimplementedError("JSON representation not supported");
}

DriverSpec::~DriverSpec() = default;

Result<IndexDomain<>> RegisteredDriverBase::SpecGetDomain(
    const DriverSpecCommonData& spec) {
  return spec.schema.domain();
}

Result<ChunkLayout> RegisteredDriverBase::SpecGetChunkLayout(
    const DriverSpecCommonData& spec) {
  return spec.schema.chunk_layout();
}

Result<CodecSpec::Ptr> RegisteredDriverBase::SpecGetCodec(
    const DriverSpecCommonData& spec) {
  return spec.schema.codec();
}

Result<SharedArray<const void>> RegisteredDriverBase::SpecGetFillValue(
    const DriverSpecCommonData& spec, IndexTransformView<> transform) {
  auto& schema = spec.schema;
  auto fill_value = schema.fill_value();
  if (!fill_value.valid()) return {std::in_place};
  if (!transform.valid()) {
    return SharedArray<const void>(fill_value.shared_array_view());
  }
  return TransformOutputBroadcastableArray(transform, std::move(fill_value),
                                           schema.domain());
}

DriverSpec::Bound::~Bound() = default;

absl::Status ApplyOptions(DriverSpec::Ptr& spec, SpecOptions&& options) {
  if (spec->use_count() != 1) spec = spec->Clone();
  return spec->ApplyOptions(std::move(options));
}

namespace {
absl::Status MaybeDeriveTransform(TransformedDriverSpec<>& spec) {
  TENSORSTORE_ASSIGN_OR_RETURN(auto domain, spec.driver_spec->GetDomain());
  if (domain.valid()) {
    spec.transform = IdentityTransform(domain);
  }
  return absl::OkStatus();
}
}  // namespace

absl::Status TransformAndApplyOptions(TransformedDriverSpec<>& spec,
                                      SpecOptions&& options) {
  const bool should_get_transform =
      !spec.transform.valid() && options.domain().valid();
  TENSORSTORE_RETURN_IF_ERROR(
      options.TransformInputSpaceSchema(spec.transform));
  TENSORSTORE_RETURN_IF_ERROR(
      ApplyOptions(spec.driver_spec, std::move(options)));
  if (should_get_transform) {
    TENSORSTORE_RETURN_IF_ERROR(MaybeDeriveTransform(spec));
  }
  return absl::OkStatus();
}

Result<IndexDomain<>> GetEffectiveDomain(const TransformedDriverSpec<>& spec) {
  if (!spec.driver_spec) return {std::in_place};
  if (!spec.transform.valid()) {
    return spec.driver_spec->GetDomain();
  } else {
    return spec.transform.domain();
  }
}

Result<ChunkLayout> GetEffectiveChunkLayout(
    const TransformedDriverSpec<>& spec) {
  if (!spec.driver_spec) return {std::in_place};
  TENSORSTORE_ASSIGN_OR_RETURN(auto chunk_layout,
                               spec.driver_spec->GetChunkLayout());
  if (spec.transform.valid()) {
    TENSORSTORE_ASSIGN_OR_RETURN(chunk_layout,
                                 std::move(chunk_layout) | spec.transform);
  }
  return chunk_layout;
}

Result<SharedArray<const void>> GetEffectiveFillValue(
    const TransformedDriverSpec<>& spec) {
  if (!spec.driver_spec) return {std::in_place};
  return spec.driver_spec->GetFillValue(spec.transform);
}

Result<CodecSpec::Ptr> GetEffectiveCodec(const TransformedDriverSpec<>& spec) {
  if (!spec.driver_spec) return {std::in_place};
  return spec.driver_spec->GetCodec();
}

Result<Schema> GetEffectiveSchema(const TransformedDriverSpec<>& spec) {
  if (!spec.driver_spec) return {std::in_place};
  Schema schema;
  TENSORSTORE_RETURN_IF_ERROR(schema.Set(spec.driver_spec->schema().dtype()));
  TENSORSTORE_RETURN_IF_ERROR(schema.Set(spec.driver_spec->schema().rank()));
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto domain, GetEffectiveDomain(spec));
    TENSORSTORE_RETURN_IF_ERROR(schema.Set(domain));
  }
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto chunk_layout,
                                 GetEffectiveChunkLayout(spec));
    TENSORSTORE_RETURN_IF_ERROR(schema.Set(std::move(chunk_layout)));
  }
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto codec, spec.driver_spec->GetCodec());
    TENSORSTORE_RETURN_IF_ERROR(schema.Set(std::move(codec)));
  }
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto fill_value, GetEffectiveFillValue(spec));
    TENSORSTORE_RETURN_IF_ERROR(
        schema.Set(Schema::FillValue(std::move(fill_value))));
  }
  return schema;
}

template <template <typename> class MaybeBound>
DimensionIndex GetRank(const TransformedDriverSpec<MaybeBound>& spec) {
  if (spec.transform.valid()) return spec.transform.input_rank();
  if (spec.driver_spec) return spec.driver_spec->schema().rank();
  return dynamic_rank;
}

#define TENSORSTORE_INTERNAL_DO_INSTANTIATE(MaybeBound) \
  template DimensionIndex GetRank<MaybeBound>(          \
      const TransformedDriverSpec<MaybeBound>& spec);   \
  /**/
TENSORSTORE_INTERNAL_DO_INSTANTIATE(ContextBound)
TENSORSTORE_INTERNAL_DO_INSTANTIATE(ContextUnbound)
#undef TENSORSTORE_INTERNAL_DO_INSTANTIATE

Future<Driver::Handle> OpenDriver(TransformedDriverSpec<> spec,
                                  TransactionalOpenOptions&& options) {
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto open_transaction,
      internal::AcquireOpenTransactionPtrOrError(options.transaction));
  return internal::OpenDriver(std::move(open_transaction), std::move(spec),
                              std::move(options));
}

Future<Driver::Handle> OpenDriver(OpenTransactionPtr transaction,
                                  TransformedDriverSpec<> spec,
                                  OpenOptions&& options) {
  TENSORSTORE_RETURN_IF_ERROR(internal::TransformAndApplyOptions(
      spec,
      // Moves out just the `SpecOptions` base.  The members of the derived
      // class `OpenOptions`, like `context` and `read_write_mode`, are
      // retained.
      static_cast<SpecOptions&&>(options)));
  if (!options.context) {
    options.context = Context::Default();
  }
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto bound_spec, spec.driver_spec->Bind(std::move(options.context)));
  return internal::OpenDriver(
      std::move(transaction),
      {std::move(bound_spec), std::move(spec.transform)},
      options.read_write_mode);
}

Future<Driver::Handle> OpenDriver(
    OpenTransactionPtr transaction,
    TransformedDriverSpec<ContextBound> bound_spec,
    ReadWriteMode read_write_mode) {
  return MapFutureValue(
      InlineExecutor{},
      [transform = std::move(bound_spec.transform)](
          Driver::Handle handle) mutable -> Result<Driver::Handle> {
        if (transform.valid()) {
          TENSORSTORE_ASSIGN_OR_RETURN(
              handle.transform,
              tensorstore::ComposeTransforms(std::move(handle.transform),
                                             std::move(transform)));
        }
        return handle;
      },
      bound_spec.driver_spec->Open(std::move(transaction), read_write_mode));
}

Driver::~Driver() = default;

Result<TransformedDriverSpec<>> Driver::GetSpec(
    internal::OpenTransactionPtr transaction, IndexTransformView<> transform,
    SpecOptions&& options, const ContextSpecBuilder& context_builder) {
  TENSORSTORE_ASSIGN_OR_RETURN(auto transformed_bound_spec,
                               GetBoundSpec(std::move(transaction), transform));
  TransformedDriverSpec<> transformed_spec;
  transformed_spec.driver_spec =
      transformed_bound_spec.driver_spec->Unbind(context_builder);
  transformed_spec.transform = std::move(transformed_bound_spec).transform;
  TENSORSTORE_RETURN_IF_ERROR(
      internal::TransformAndApplyOptions(transformed_spec, std::move(options)));
  return transformed_spec;
}

Result<TransformedDriverSpec<ContextBound>> Driver::GetBoundSpec(
    internal::OpenTransactionPtr transaction, IndexTransformView<> transform) {
  return absl::UnimplementedError("JSON representation not supported");
}

Result<ChunkLayout> Driver::GetChunkLayout(IndexTransformView<> transform) {
  return {std::in_place};
}

Result<CodecSpec::Ptr> Driver::GetCodec() { return CodecSpec::Ptr{}; }

Result<SharedArray<const void>> Driver::GetFillValue(
    IndexTransformView<> transform) {
  return {std::in_place};
}

Future<IndexTransform<>> Driver::ResolveBounds(OpenTransactionPtr transaction,
                                               IndexTransform<> transform,
                                               ResolveBoundsOptions options) {
  return std::move(transform);
}

void Driver::Read(internal::OpenTransactionPtr transaction,
                  IndexTransform<> transform, ReadChunkReceiver receiver) {
  execution::set_error(FlowSingleReceiver{std::move(receiver)},
                       absl::UnimplementedError("Reading not supported"));
}

void Driver::Write(internal::OpenTransactionPtr transaction,
                   IndexTransform<> transform, WriteChunkReceiver receiver) {
  execution::set_error(FlowSingleReceiver{std::move(receiver)},
                       absl::UnimplementedError("Writing not supported"));
}

Future<IndexTransform<>> Driver::Resize(OpenTransactionPtr transaction,
                                        IndexTransform<> transform,
                                        span<const Index> inclusive_min,
                                        span<const Index> exclusive_max,
                                        ResizeOptions options) {
  return absl::UnimplementedError("Resize not supported");
}

namespace {
auto SchemaExcludingRankAndDtypeJsonBinder() {
  return jb::DefaultInitializedValue(
      [](auto is_loading, auto options, auto* obj, auto* j) {
        if constexpr (!is_loading) {
          // Set default dtype and rank to the actual dtype/rank to prevent them
          // from being included in json, since they are already included in the
          // separate `dtype` and `rank` members of the Spec.
          options.Set(obj->dtype());
          options.Set(obj->rank());
        }
        return jb::DefaultBinder<>(is_loading, options, obj, j);
      });
}
}  // namespace

TENSORSTORE_DEFINE_JSON_BINDER(
    TransformedDriverSpecJsonBinder,
    [](auto is_loading, const auto& options, auto* obj,
       ::nlohmann::json* j) -> Status {
      auto& registry = internal::GetDriverRegistry();
      return jb::Object(
          jb::Member("driver",
                     jb::Projection(&TransformedDriverSpec<>::driver_spec,
                                    registry.KeyBinder())),
          jb::Projection(
              [](auto& obj) -> decltype(auto) { return (*obj.driver_spec); },
              jb::Sequence(
                  jb::Member("context",
                             jb::Projection(
                                 &internal::DriverSpec::context_spec_,
                                 internal::ContextSpecDefaultableJsonBinder)),
                  jb::Member("schema",
                             jb::Projection(
                                 [](auto& x) -> decltype(auto) {
                                   return (x.schema());
                                 },
                                 SchemaExcludingRankAndDtypeJsonBinder())),
                  jb::Member("dtype",
                             jb::GetterSetter(
                                 [](auto& x) { return x.schema().dtype(); },
                                 [](auto& x, DataType value) {
                                   return x.schema().Set(value);
                                 },
                                 jb::ConstrainedDataTypeJsonBinder)))),
          jb::OptionalMember(
              "transform", jb::Projection(&TransformedDriverSpec<>::transform)),
          jb::OptionalMember(
              "rank",
              jb::GetterSetter(
                  [](const auto& obj) {
                    return obj.transform.valid()
                               ? static_cast<DimensionIndex>(dynamic_rank)
                               : static_cast<DimensionIndex>(
                                     obj.driver_spec->schema().rank());
                  },
                  [](const auto& obj, DimensionIndex rank) {
                    if (rank != dynamic_rank) {
                      if (obj.transform.valid()) {
                        if (obj.transform.input_rank() != rank) {
                          return absl::InvalidArgumentError(tensorstore::StrCat(
                              "Specified rank (", rank,
                              ") does not match input rank of transform (",
                              obj.transform.input_rank(), ")"));
                        }
                      } else {
                        TENSORSTORE_RETURN_IF_ERROR(
                            obj.driver_spec->schema().Set(
                                RankConstraint{rank}));
                      }
                    }
                    return absl::OkStatus();
                  },
                  jb::ConstrainedRankJsonBinder)),
          jb::Initialize([](auto* obj) {
            if (!obj->transform.valid()) return absl::OkStatus();
            return obj->driver_spec->schema().Set(
                RankConstraint{obj->transform.output_rank()});
          }),
          jb::Projection(&TransformedDriverSpec<>::driver_spec,
                         registry.RegisteredObjectBinder()),
          jb::Initialize([](auto* obj) {
            if (obj->transform.valid()) return absl::OkStatus();
            return MaybeDeriveTransform(*obj);
          }))(is_loading, options, obj, j);
    })

namespace {

/// If `promise` does not already have a result set, sets its result to `status`
/// and sets `promise.result_needed() = false`.
///
/// This does not cause `promise.ready()` to become `true`.  The corresponding
/// `Future` will become ready when the last `Promise` reference is released.
template <typename T>
void SetErrorWithoutCommit(const Promise<T>& promise, Status error) {
  if (internal_future::FutureAccess::rep(promise).LockResult()) {
    promise.raw_result() = std::move(error);
  }
}

/// Local state for the asynchronous operation initiated by the two `DriverRead`
/// overloads.
///
/// `DriverRead` asynchronously performs the following steps:
///
/// 1. Resolves the bounds in `source` via `Driver::ResolveBounds`.  When
///    completed, control continues with `DriverReadIntoExistingInitiateOp` (if
///    using an existing `target` array) or `DriverReadIntoNewInitiateOp` (if
///    using a new `target` array).
///
/// 2. If reading into an existing `target` array, validates that the resolved
///    source bounds match the normalized bounds of the `target` array.
///    Otherwise, allocates a new `target` array with a domain given by the
///    source bounds.
///
/// 3. Calls `Driver::Read` with a `ReadChunkReceiver` to initiate the actual
///    read over the resolved `source.transform` bounds.  `ReadChunkReceiver`
///    ensures that the read is canceled if `promise.result_needed()` becomes
///    `false`.
///
/// 4. For each `ReadChunk` received, `ReadChunkReceiver` invokes `ReadChunkOp`
///    using `executor` to copy the data from the `ReadChunk` to the appropriate
///    portion of the `target` array.
///
/// 5. Once all work has finished (either because all chunks were processed
///    successfully, an error occurred, or all references to the future
///    associated with `promise` were released), all references to `ReadState`
///    are released, which in turn releases all references to `promise`, which
///    causes `promise` to become ready.  Note that `promise` is never marked
///    ready, even with an error, while the `target` array may still be
///    accessed, because the user is permitted to destroy or reuse the `target`
///    array as soon as the promise becomes ready.
template <typename PromiseValue>
struct ReadState
    : public internal::AtomicReferenceCount<ReadState<PromiseValue>> {
  Executor executor;
  Driver::Ptr source_driver;
  internal::OpenTransactionPtr source_transaction;
  DataTypeConversionLookupResult data_type_conversion;
  NormalizedTransformedArray<Shared<void>> target;
  DomainAlignmentOptions alignment_options;
  ReadProgressFunction read_progress_function;
  Promise<PromiseValue> promise;
  std::atomic<Index> copied_elements{0};
  Index total_elements;

  void SetError(Status error) {
    SetErrorWithoutCommit(promise, std::move(error));
  }

  void UpdateProgress(Index num_elements) {
    if (!read_progress_function) return;
    read_progress_function(
        ReadProgress{total_elements, copied_elements += num_elements});
  }
};

/// Callback invoked by `ReadChunkReceiver` (using the executor) to copy data
/// from a single `ReadChunk` to the appropriate portion of the `target` array.
template <typename PromiseValue>
struct ReadChunkOp {
  IntrusivePtr<ReadState<PromiseValue>> state;
  ReadChunk chunk;
  IndexTransform<> cell_transform;
  void operator()() {
    // Map the portion of the target array that corresponds to this chunk to
    // the index space expected by the chunk.
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto target,
        ApplyIndexTransform(std::move(cell_transform), state->target),
        state->SetError(_));
    Status copy_status =
        internal::CopyReadChunk(chunk.impl, std::move(chunk.transform),
                                state->data_type_conversion, target);
    if (copy_status.ok()) {
      state->UpdateProgress(ProductOfExtents(target.shape()));
    } else {
      state->SetError(std::move(copy_status));
    }
  }
};

/// FlowReceiver used by the two `DriverRead` overloads to copy data from chunks
/// as they become available.
template <typename PromiseValue>
struct ReadChunkReceiver {
  IntrusivePtr<ReadState<PromiseValue>> state;
  FutureCallbackRegistration cancel_registration;
  void set_starting(AnyCancelReceiver cancel) {
    cancel_registration =
        state->promise.ExecuteWhenNotNeeded(std::move(cancel));
  }
  void set_stopping() { cancel_registration(); }
  void set_done() {}
  void set_error(Status error) { state->SetError(std::move(error)); }
  void set_value(ReadChunk chunk, IndexTransform<> cell_transform) {
    // Defer all work to the executor, because we don't know on which thread
    // this may be called.
    state->executor(ReadChunkOp<PromiseValue>{state, std::move(chunk),
                                              std::move(cell_transform)});
  }
};

/// Callback used by `DriverRead` to initiate a read into an existing array once
/// the source transform bounds have been resolved.
struct DriverReadIntoExistingInitiateOp {
  using State = ReadState<void>;
  IntrusivePtr<State> state;
  void operator()(Promise<void> promise,
                  ReadyFuture<IndexTransform<>> source_transform_future) {
    IndexTransform<> source_transform =
        std::move(source_transform_future.value());
    // Align the resolved bounds to `target`.
    TENSORSTORE_ASSIGN_OR_RETURN(
        source_transform,
        AlignTransformTo(std::move(source_transform), state->target.domain(),
                         state->alignment_options),
        static_cast<void>(promise.SetResult(_)));
    state->promise = std::move(promise);
    state->total_elements = source_transform.domain().num_elements();

    // Initiate the read on the driver.
    auto source_driver = std::move(state->source_driver);
    auto source_transaction = std::move(state->source_transaction);
    source_driver->Read(std::move(source_transaction),
                        std::move(source_transform),
                        ReadChunkReceiver<void>{std::move(state)});
  }
};

/// Callback used by `DriverRead` to initiate a read into a new array once the
/// source transform bounds have been resolved.
struct DriverReadIntoNewInitiateOp {
  using State = ReadState<SharedOffsetArray<void>>;
  IntrusivePtr<State> state;
  DataType target_dtype;
  ContiguousLayoutOrder target_layout_order;
  void operator()(Promise<SharedOffsetArray<void>> promise,
                  ReadyFuture<IndexTransform<>> source_transform_future) {
    IndexTransform<> source_transform =
        std::move(source_transform_future.value());
    auto array = AllocateArray(source_transform.domain().box(),
                               target_layout_order, default_init, target_dtype);
    auto& r = promise.raw_result() = array;
    state->target = MakeNormalizedTransformedArray(*r);
    state->promise = std::move(promise);
    state->total_elements = source_transform.input_domain().num_elements();

    // Initiate the read on the driver.
    auto source_driver = std::move(state->source_driver);
    auto source_transaction = std::move(state->source_transaction);
    source_driver->Read(
        std::move(source_transaction), std::move(source_transform),
        ReadChunkReceiver<SharedOffsetArray<void>>{std::move(state)});
  }
};

}  // namespace

Future<void> DriverRead(Executor executor, DriverHandle source,
                        TransformedSharedArrayView<void> target,
                        DriverReadOptions options) {
  TENSORSTORE_RETURN_IF_ERROR(
      internal::ValidateSupportsRead(source.driver.read_write_mode()));
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto normalized_target,
      MakeNormalizedTransformedArray(std::move(target)));
  using State = ReadState<void>;
  IntrusivePtr<State> state(new State);
  state->executor = executor;
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->data_type_conversion,
      GetDataTypeConverterOrError(source.driver->dtype(),
                                  normalized_target.dtype(),
                                  options.data_type_conversion_flags));
  state->source_driver = std::move(source.driver);
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->source_transaction,
      internal::AcquireOpenTransactionPtrOrError(source.transaction));
  state->target = std::move(normalized_target);
  state->alignment_options = options.alignment_options;
  state->read_progress_function = std::move(options.progress_function);
  auto pair = PromiseFuturePair<void>::Make(MakeResult());

  // Resolve the bounds for `source.transform`.
  auto transform_future = state->source_driver->ResolveBounds(
      state->source_transaction, std::move(source.transform),
      fix_resizable_bounds);

  // Initiate the read once the bounds have been resolved.
  LinkValue(WithExecutor(std::move(executor),
                         DriverReadIntoExistingInitiateOp{std::move(state)}),
            std::move(pair.promise), std::move(transform_future));
  return std::move(pair.future);
}

Future<void> DriverRead(DriverHandle source,
                        TransformedSharedArrayView<void> target,
                        ReadOptions options) {
  auto executor = source.driver->data_copy_executor();
  return internal::DriverRead(
      std::move(executor), std::move(source), std::move(target), /*options=*/
      {/*.progress_function=*/std::move(options.progress_function),
       /*.alignment_options=*/options.alignment_options});
}

Future<SharedOffsetArray<void>> DriverRead(
    Executor executor, DriverHandle source, DataType target_dtype,
    ContiguousLayoutOrder target_layout_order,
    DriverReadIntoNewOptions options) {
  TENSORSTORE_RETURN_IF_ERROR(
      internal::ValidateSupportsRead(source.driver.read_write_mode()));
  using State = ReadState<SharedOffsetArray<void>>;
  IntrusivePtr<State> state(new State);
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->data_type_conversion,
      GetDataTypeConverterOrError(source.driver->dtype(), target_dtype));
  state->executor = executor;
  state->source_driver = std::move(source.driver);
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->source_transaction,
      internal::AcquireOpenTransactionPtrOrError(source.transaction));
  state->read_progress_function = std::move(options.progress_function);
  auto pair = PromiseFuturePair<SharedOffsetArray<void>>::Make();

  // Resolve the bounds for `source.transform`.
  auto transform_future = state->source_driver->ResolveBounds(
      state->source_transaction, std::move(source.transform),
      fix_resizable_bounds);

  // Initiate the read once the bounds have been resolved.
  LinkValue(
      WithExecutor(std::move(executor),
                   DriverReadIntoNewInitiateOp{std::move(state), target_dtype,
                                               target_layout_order}),
      std::move(pair.promise), std::move(transform_future));
  return std::move(pair.future);
}

Future<SharedOffsetArray<void>> DriverRead(DriverHandle source,
                                           ReadIntoNewArrayOptions options) {
  auto dtype = source.driver->dtype();
  auto executor = source.driver->data_copy_executor();
  return internal::DriverRead(
      std::move(executor), std::move(source), dtype, options.layout_order,
      /*options=*/
      {/*.progress_function=*/std::move(options.progress_function)});
}

namespace {

/// Local state for the asynchronous operation initiated by the `DriverWrite`
/// function.
///
/// `DriverWrite` asynchronously performs the following steps:
///
/// 1. Resolves the `target_transform` bounds from the `DriverWriteTarget`.
///    When completed, control continues with `DriverWriteInitiateOp`.
///
/// 2. Validates that the resolved target bounds match the normalized bounds of
///    the `source` array.
///
/// 3. Calls `Driver::Write` with a `WriteChunkReceiver` to initiate the actual
///    write over the resolved `target_transform` bounds.  `WriteChunkReceiver`
///    ensures that the write is canceled when `copy_promise.result_needed()`
///    becomes `false`.
///
/// 4. For each `WriteChunk` received, `WriteChunkReceiver` invokes
///    `WriteChunkOp` using `executor` to copy the data from the appropriate
///    portion of the `source` array to the `WriteChunk`.
///
/// 5. `WriteChunkOp` links the writeback `Future` returned from the write
///    operation on `WriteChunk` to `copy_promise` with a `CommitCallback` that
///    holds a reference-counted pointer to `CommitState` (but not to
///    `WriteState`).
///
/// 5. Once all `WriteChunkOp` calls have completed (either successfully or with
///    an error), all references to `WriteState` are released, causing it to be
///    destroyed, which in turn releases all references to `copy_promise`, which
///    causes `copy_promise` to become ready.  `CommitCallback` calls may,
///    however, still be outstanding at this point.  Note that `copy_promise` is
///    never marked ready, even with an error, while the `source` array may
///    still be accessed, because the user is permitted to destroy or reuse the
///    `source` array as soon as `copy_promise` becomes ready.
///
/// 6. Once `WriteState` is destroyed and all `CommitCallback` links are
///    completed, the `commit_promise` is marked ready, indicating to the caller
///    that all data has been written back (or an error has occurred).
struct WriteState : public internal::AtomicReferenceCount<WriteState> {
  /// CommitState is a separate reference-counted struct (rather than simply
  /// using `WriteState`) in order to ensure the reference to `copy_promise` and
  /// `source` are released once copying has completed (in order for
  /// `copy_promise` to become ready and for any memory used by `source`, if not
  /// otherwise referenced, to be freed).
  struct CommitState : public internal::AtomicReferenceCount<CommitState> {
    WriteProgressFunction write_progress_function;
    Index total_elements;
    std::atomic<Index> copied_elements{0};
    std::atomic<Index> committed_elements{0};

    void UpdateCopyProgress(Index num_elements) {
      if (!write_progress_function) return;
      write_progress_function(WriteProgress{
          total_elements, copied_elements += num_elements, committed_elements});
    }

    void UpdateCommitProgress(Index num_elements) {
      if (!write_progress_function) return;
      write_progress_function(WriteProgress{
          total_elements, copied_elements, committed_elements += num_elements});
    }
  };
  Executor executor;
  NormalizedTransformedArray<Shared<const void>> source;
  DataTypeConversionLookupResult data_type_conversion;
  Driver::Ptr target_driver;
  internal::OpenTransactionPtr target_transaction;
  DomainAlignmentOptions alignment_options;
  Promise<void> copy_promise;
  Promise<void> commit_promise;
  IntrusivePtr<CommitState> commit_state{new CommitState};

  void SetError(Status error) {
    SetErrorWithoutCommit(copy_promise, std::move(error));
  }
};

/// Callback invoked by `WriteChunkReceiver` (using the executor) to copy data
/// from the appropriate portion of the source array to a single `WriteChunk`.
struct WriteChunkOp {
  IntrusivePtr<WriteState> state;
  WriteChunk chunk;
  IndexTransform<> cell_transform;
  void operator()() {
    // Map the portion of the source array that corresponds to this chunk
    // to the index space expected by the chunk.
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto source,
        ApplyIndexTransform(std::move(cell_transform), state->source),
        state->SetError(_));

    DefaultNDIterableArena arena;

    TENSORSTORE_ASSIGN_OR_RETURN(
        auto source_iterable,
        GetNormalizedTransformedArrayNDIterable(std::move(source), arena),
        state->SetError(_));

    LockCollection lock_collection;

    absl::Status copy_status;
    Future<const void> commit_future;

    {
      TENSORSTORE_ASSIGN_OR_RETURN(auto guard,
                                   LockChunks(lock_collection, chunk.impl),
                                   state->SetError(_));

      TENSORSTORE_ASSIGN_OR_RETURN(
          auto target_iterable,
          chunk.impl(WriteChunk::BeginWrite{}, chunk.transform, arena),
          state->SetError(_));

      source_iterable = GetConvertedInputNDIterable(
          std::move(source_iterable), target_iterable->dtype(),
          state->data_type_conversion);

      NDIterableCopier copier(*source_iterable, *target_iterable,
                              chunk.transform.input_shape(), arena);
      copy_status = copier.Copy();
      auto end_write_result =
          chunk.impl(WriteChunk::EndWrite{}, chunk.transform,
                     copier.layout_info().layout_view(),
                     copier.stepper().position(), arena);
      commit_future = std::move(end_write_result.commit_future);
      if (copy_status.ok()) {
        copy_status = std::move(end_write_result.copy_status);
      }
    }

    if (copy_status.ok()) {
      const Index num_elements = chunk.transform.input_domain().num_elements();
      state->commit_state->UpdateCopyProgress(num_elements);
      struct CommitCallback {
        IntrusivePtr<WriteState::CommitState> state;
        Index num_elements;
        void operator()(Promise<void>, Future<const void>) const {
          state->UpdateCommitProgress(num_elements);
        }
      };
      if (state->commit_promise.valid() && commit_future.valid()) {
        // For transactional writes, `state->commit_promise` is null.
        LinkValue(CommitCallback{state->commit_state, num_elements},
                  state->commit_promise, std::move(commit_future));
      } else {
        state->commit_state->UpdateCommitProgress(num_elements);
      }
    } else {
      state->SetError(std::move(copy_status));
    }
  }
};

/// FlowReceiver used by `DriverWrite` to copy data from the source array to
/// chunks as they become available.
struct WriteChunkReceiver {
  IntrusivePtr<WriteState> state;
  FutureCallbackRegistration cancel_registration;
  void set_starting(AnyCancelReceiver cancel) {
    cancel_registration =
        state->copy_promise.ExecuteWhenNotNeeded(std::move(cancel));
  }
  void set_stopping() { cancel_registration(); }
  void set_done() {}
  void set_error(Status error) { state->SetError(std::move(error)); }
  void set_value(WriteChunk chunk, IndexTransform<> cell_transform) {
    // Defer all work to the executor, because we don't know on which thread
    // this may be called.
    //
    // Dont't move `state` since `set_value` may be called multiple times.
    state->executor(
        WriteChunkOp{state, std::move(chunk), std::move(cell_transform)});
  }
};

/// Callback used by `DriverWrite` to initiate the write once the target
/// transform bounds have been resolved.
struct DriverWriteInitiateOp {
  IntrusivePtr<WriteState> state;
  void operator()(Promise<void> promise,
                  ReadyFuture<IndexTransform<>> target_transform_future) {
    IndexTransform<> target_transform =
        std::move(target_transform_future.value());
    // Align `source` to the resolved bounds.
    TENSORSTORE_ASSIGN_OR_RETURN(
        state->source.transform(),
        AlignTransformTo(std::move(state->source.transform()),
                         target_transform.domain(), state->alignment_options),
        static_cast<void>(promise.SetResult(_)));
    state->commit_state->total_elements =
        target_transform.domain().num_elements();
    state->copy_promise = std::move(promise);

    // Initiate the write on the driver.
    auto target_driver = std::move(state->target_driver);
    auto target_transaction = std::move(state->target_transaction);
    target_driver->Write(std::move(target_transaction),
                         std::move(target_transform),
                         WriteChunkReceiver{std::move(state)});
  }
};

}  // namespace

WriteFutures DriverWrite(Executor executor,
                         TransformedSharedArrayView<const void> source,
                         DriverHandle target, DriverWriteOptions options) {
  TENSORSTORE_RETURN_IF_ERROR(
      internal::ValidateSupportsWrite(target.driver.read_write_mode()));
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto normalized_source,
      MakeNormalizedTransformedArray(std::move(source)));
  IntrusivePtr<WriteState> state(new WriteState);
  state->executor = executor;
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->data_type_conversion,
      GetDataTypeConverterOrError(normalized_source.dtype(),
                                  target.driver->dtype(),
                                  options.data_type_conversion_flags));
  state->target_driver = std::move(target.driver);
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->target_transaction,
      internal::AcquireOpenTransactionPtrOrError(target.transaction));
  state->source = std::move(normalized_source);
  state->alignment_options = options.alignment_options;
  state->commit_state->write_progress_function =
      std::move(options.progress_function);
  auto copy_pair = PromiseFuturePair<void>::Make(MakeResult());
  PromiseFuturePair<void> commit_pair;
  if (!state->target_transaction) {
    commit_pair =
        PromiseFuturePair<void>::LinkError(MakeResult(), copy_pair.future);
    state->commit_promise = std::move(commit_pair.promise);
  } else {
    commit_pair.future = copy_pair.future;
  }

  // Resolve the bounds for `target.transform`.
  auto transform_future = state->target_driver->ResolveBounds(
      state->target_transaction, std::move(target.transform),
      fix_resizable_bounds);

  // Initiate the write once the bounds have been resolved.
  LinkValue(WithExecutor(std::move(executor),
                         DriverWriteInitiateOp{std::move(state)}),
            std::move(copy_pair.promise), std::move(transform_future));
  return {std::move(copy_pair.future), std::move(commit_pair.future)};
}

WriteFutures DriverWrite(TransformedSharedArrayView<const void> source,
                         DriverHandle target, WriteOptions options) {
  auto executor = target.driver->data_copy_executor();
  return internal::DriverWrite(
      std::move(executor), std::move(source), std::move(target),
      /*options=*/
      {/*.progress_function=*/std::move(options.progress_function),
       /*.alignment_options=*/options.alignment_options});
}

namespace {

/// Local state for the asynchronous operation initiated by `DriverCopy`.
///
/// `DriverCopy` asynchronously performs the following steps:
///
/// 1. Resolves the `source_transform` bounds from the `DriverReadSource` and
///    the `target_transform` bounds from the `DriverWriteTarget`.  When
///    completed, control continues with `DriverCopyInitiateOp`.
///
/// 2. Validates that the resolved source and target bounds match.
///
/// 3. Calls `Driver::Read` on the `source_driver` with a
///    `CopyReadChunkReceiver` to initiate the actual read over the resolved
///    `source_transform` bounds.  `CopyReadChunkReceiver` ensures that the read
///    is canceled if `copy_promise.result_needed()` becomes `false`.
///
/// 4. For each `ReadChunk` received, `CopyReadChunkReceiver` invokes
///    `CopyInitiateWriteOp` using `executor`: `CopyInitiateWriteOp` calls
///    `Driver::Write` on `target_driver` with a `CopyWriteChunkReceiver` to
///    initiate the write to the portion of `target_driver` corresponding to the
///    `ReadChunk`.  `CopyWriteChunkReceiver` ensures that the write is canceled
///    if `copy_promise.result_needed()` becomes `false`.
///
/// 5. For each `WriteChunk` received, `CopyWriteChunkReceiver` invokes
///    `CopyChunkOp` using executor to copy the data from the appropriate
///    portion of the `ReadChunk` to the `WriteChunk`.
///
/// 6. `CopyChunkOp` links the writeback `Future` returned from the write
///    operation on `WriteChunk` to `copy_promise` with a `CommitCallback` that
///    holds a reference-counted pointer to `CommitState` (but not to
///    `WriteState`).
///
/// 7. Once all `CopyChunkOp` calls have completed (either successfully or with
///    an error), all references to `CopyState` are released, causing it to be
///    destroyed, which in turn releases all references to `copy_promise`, which
///    causes `copy_promise` to become ready.  `CommitCallback` calls may,
///    however, still be outstanding at this point.  Note that `copy_promise` is
///    never marked ready, even with an error, while the `source` array may
///    still be accessed, because the user is permitted to destroy or reuse the
///    `source` array as soon as `copy_promise` becomes ready.
///
/// 8. Once `CopyState` is destroyed and all `CommitCallback` links are
///    completed, the `commit_promise` is marked ready, indicating to the caller
///    that all data has been written back (or an error has occurred).
struct CopyState : public internal::AtomicReferenceCount<CopyState> {
  /// CommitState is a separate reference-counted struct (rather than simply
  /// using `CopyState`) in order to ensure the reference to `copy_promise` and
  /// `source` are released once copying has completed (in order for
  /// `copy_promise` to become ready and for `source`, if not otherwise
  /// referenced, to be freed).
  struct CommitState : public internal::AtomicReferenceCount<CommitState> {
    CopyProgressFunction progress_function;
    Index total_elements;
    std::atomic<Index> copied_elements{0};
    std::atomic<Index> committed_elements{0};
    std::atomic<Index> read_elements{0};

    void UpdateReadProgress(Index num_elements) {
      if (!progress_function) return;
      progress_function(CopyProgress{total_elements,
                                     read_elements += num_elements,
                                     copied_elements, committed_elements});
    }

    void UpdateCopyProgress(Index num_elements) {
      if (!progress_function) return;
      progress_function(CopyProgress{total_elements, read_elements,
                                     copied_elements += num_elements,
                                     committed_elements});
    }

    void UpdateCommitProgress(Index num_elements) {
      if (!progress_function) return;
      progress_function(CopyProgress{total_elements, read_elements,
                                     copied_elements,
                                     committed_elements += num_elements});
    }
  };
  Executor executor;
  Driver::Ptr source_driver;
  internal::OpenTransactionPtr source_transaction;
  DataTypeConversionLookupResult data_type_conversion;
  Driver::Ptr target_driver;
  internal::OpenTransactionPtr target_transaction;
  IndexTransform<> target_transform;
  DomainAlignmentOptions alignment_options;
  Promise<void> copy_promise;
  Promise<void> commit_promise;
  IntrusivePtr<CommitState> commit_state{new CommitState};

  void SetError(Status error) {
    SetErrorWithoutCommit(copy_promise, std::move(error));
  }
};

/// Callback invoked by `CopyWriteChunkReceiver` (using the executor) to copy
/// data from the relevant portion of a single `ReadChunk` to a `WriteChunk`.
struct CopyChunkOp {
  IntrusivePtr<CopyState> state;
  ReadChunk adjusted_read_chunk;
  WriteChunk write_chunk;
  void operator()() {
    DefaultNDIterableArena arena;

    LockCollection lock_collection;

    absl::Status copy_status;
    Future<const void> commit_future;
    {
      TENSORSTORE_ASSIGN_OR_RETURN(
          auto guard,
          LockChunks(lock_collection, adjusted_read_chunk.impl,
                     write_chunk.impl),
          state->SetError(_));

      TENSORSTORE_ASSIGN_OR_RETURN(
          auto source_iterable,
          adjusted_read_chunk.impl(ReadChunk::BeginRead{},
                                   std::move(adjusted_read_chunk.transform),
                                   arena),
          state->SetError(_));

      TENSORSTORE_ASSIGN_OR_RETURN(
          auto target_iterable,
          write_chunk.impl(WriteChunk::BeginWrite{}, write_chunk.transform,
                           arena),
          state->SetError(_));

      source_iterable = GetConvertedInputNDIterable(
          std::move(source_iterable), target_iterable->dtype(),
          state->data_type_conversion);

      NDIterableCopier copier(*source_iterable, *target_iterable,
                              write_chunk.transform.input_shape(), arena);
      copy_status = copier.Copy();

      auto end_write_result =
          write_chunk.impl(WriteChunk::EndWrite{}, write_chunk.transform,
                           copier.layout_info().layout_view(),
                           copier.stepper().position(), arena);
      commit_future = std::move(end_write_result.commit_future);
      if (copy_status.ok()) {
        copy_status = std::move(end_write_result.copy_status);
      }
    }
    if (copy_status.ok()) {
      const Index num_elements = write_chunk.transform.domain().num_elements();
      state->commit_state->UpdateCopyProgress(num_elements);
      struct CommitCallback {
        IntrusivePtr<CopyState::CommitState> state;
        Index num_elements;
        void operator()(Promise<void>, Future<const void>) const {
          state->UpdateCommitProgress(num_elements);
        }
      };
      if (state->commit_promise.valid() && commit_future.valid()) {
        // For transactional writes, `state->commit_promise` is null.
        LinkValue(CommitCallback{state->commit_state, num_elements},
                  state->commit_promise, commit_future);
      } else {
        state->commit_state->UpdateCommitProgress(num_elements);
      }
    } else {
      state->SetError(std::move(copy_status));
    }
  }
};

/// FlowReceiver used by `CopyReadChunkReceiver` to copy data from a given
/// `read_chunk` to the target `write_chunk` chunks as the target chunks become
/// available.
struct CopyWriteChunkReceiver {
  IntrusivePtr<CopyState> state;
  ReadChunk read_chunk;
  FutureCallbackRegistration cancel_registration;
  void set_starting(AnyCancelReceiver cancel) {
    cancel_registration =
        state->copy_promise.ExecuteWhenNotNeeded(std::move(cancel));
  }
  void set_stopping() { cancel_registration(); }
  void set_done() {}
  void set_error(Status error) { state->SetError(std::move(error)); }
  void set_value(WriteChunk write_chunk, IndexTransform<> cell_transform) {
    // Map the portion of the `read_chunk` that corresponds to this
    // `write_chunk` to the index space expected by `write_chunk`, and produce
    // an `adjusted_read_chunk`.
    //
    // We do this immediately, rather than deferring it to an executor, in order
    // to avoid having to make an extra copy of `read_chunk.transform`.
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto read_chunk_transform,
        ComposeTransforms(read_chunk.transform, std::move(cell_transform)),
        state->SetError(_));
    ReadChunk adjusted_read_chunk{read_chunk.impl,
                                  std::move(read_chunk_transform)};
    // Defer the actual copying to the executor.
    //
    // Dont't move `state` since `set_value` may be called multiple times.
    state->executor(CopyChunkOp{state, std::move(adjusted_read_chunk),
                                std::move(write_chunk)});
  }
};

/// Callback invoked by `CopyReadChunkReceiver` (using the executor) to initiate
/// the `Driver::Write` operation on the `target` driver corresponding to a
/// single `ReadChunk` from the `source` driver.
struct CopyInitiateWriteOp {
  IntrusivePtr<CopyState> state;
  ReadChunk chunk;
  IndexTransform<> cell_transform;
  void operator()() {
    // Map the portion of the target TensorStore corresponding to this source
    // `chunk` to the index space expected by `chunk`.
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto write_transform,
        ComposeTransforms(state->target_transform, cell_transform),
        state->SetError(_));
    state->commit_state->UpdateReadProgress(
        cell_transform.input_domain().num_elements());

    // Initiate a write for the portion of the target TensorStore
    // corresponding to this source `chunk`.
    state->target_driver->Write(
        state->target_transaction, std::move(write_transform),
        CopyWriteChunkReceiver{state, std::move(chunk)});
  }
};

/// FlowReceiver used by `DriverCopy` that receives source chunks as they become
/// available for reading, and initiates a write on the target driver for each
/// chunk received.
struct CopyReadChunkReceiver {
  IntrusivePtr<CopyState> state;
  FutureCallbackRegistration cancel_registration;
  void set_starting(AnyCancelReceiver cancel) {
    cancel_registration =
        state->copy_promise.ExecuteWhenNotNeeded(std::move(cancel));
  }
  void set_stopping() { cancel_registration(); }
  void set_done() {}
  void set_error(Status error) { state->SetError(std::move(error)); }
  void set_value(ReadChunk chunk, IndexTransform<> cell_transform) {
    // Defer actual work to executor.
    //
    // Dont't move `state` since `set_value` may be called multiple times.
    state->executor(CopyInitiateWriteOp{state, std::move(chunk),
                                        std::move(cell_transform)});
  }
};

/// Callback used by `DriverCopy` to initiate the copy operation once the bounds
/// for the source and target transforms have been resolved.
struct DriverCopyInitiateOp {
  IntrusivePtr<CopyState> state;
  void operator()(Promise<void> promise,
                  ReadyFuture<IndexTransform<>> source_transform_future,
                  ReadyFuture<IndexTransform<>> target_transform_future) {
    IndexTransform<> source_transform =
        std::move(source_transform_future.value());
    IndexTransform<> target_transform =
        std::move(target_transform_future.value());
    // Align the resolved `source_transform` domain to the resolved
    // `target_transform` domain.
    TENSORSTORE_ASSIGN_OR_RETURN(
        source_transform,
        AlignTransformTo(std::move(source_transform), target_transform.domain(),
                         state->alignment_options),
        static_cast<void>(promise.SetResult(_)));
    state->commit_state->total_elements =
        target_transform.input_domain().num_elements();
    state->copy_promise = std::move(promise);
    state->target_transform = std::move(target_transform);

    // Initiate the read operation on the source driver.
    auto source_driver = std::move(state->source_driver);
    auto source_transaction = std::move(state->source_transaction);
    source_driver->Read(std::move(source_transaction),
                        std::move(source_transform),
                        CopyReadChunkReceiver{std::move(state)});
  }
};

}  // namespace

WriteFutures DriverCopy(Executor executor, DriverHandle source,
                        DriverHandle target, DriverCopyOptions options) {
  TENSORSTORE_RETURN_IF_ERROR(
      internal::ValidateSupportsRead(source.driver.read_write_mode()));
  TENSORSTORE_RETURN_IF_ERROR(
      internal::ValidateSupportsWrite(target.driver.read_write_mode()));
  IntrusivePtr<CopyState> state(new CopyState);
  state->executor = executor;
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->data_type_conversion,
      GetDataTypeConverterOrError(source.driver->dtype(),
                                  target.driver->dtype(),
                                  options.data_type_conversion_flags));
  state->source_driver = std::move(source.driver);
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->source_transaction,
      internal::AcquireOpenTransactionPtrOrError(source.transaction));
  state->target_driver = std::move(target.driver);
  TENSORSTORE_ASSIGN_OR_RETURN(
      state->target_transaction,
      internal::AcquireOpenTransactionPtrOrError(target.transaction));
  state->alignment_options = options.alignment_options;
  state->commit_state->progress_function = std::move(options.progress_function);
  auto copy_pair = PromiseFuturePair<void>::Make(MakeResult());
  PromiseFuturePair<void> commit_pair;
  if (!state->target_transaction) {
    commit_pair =
        PromiseFuturePair<void>::LinkError(MakeResult(), copy_pair.future);
    state->commit_promise = std::move(commit_pair.promise);
  } else {
    commit_pair.future = copy_pair.future;
  }

  // Resolve the source and target bounds.
  auto source_transform_future = state->source_driver->ResolveBounds(
      state->source_transaction, std::move(source.transform),
      fix_resizable_bounds);
  auto target_transform_future = state->target_driver->ResolveBounds(
      state->target_transaction, std::move(target.transform),
      fix_resizable_bounds);

  // Initiate the copy once the bounds have been resolved.
  LinkValue(
      WithExecutor(std::move(executor), DriverCopyInitiateOp{std::move(state)}),
      std::move(copy_pair.promise), std::move(source_transform_future),
      std::move(target_transform_future));
  return {std::move(copy_pair.future), std::move(commit_pair.future)};
}

WriteFutures DriverCopy(DriverHandle source, DriverHandle target,
                        CopyOptions options) {
  auto executor = source.driver->data_copy_executor();
  return internal::DriverCopy(
      std::move(executor), std::move(source), std::move(target),
      /*options=*/
      {/*.progress_function=*/std::move(options.progress_function),
       /*.alignment_options=*/options.alignment_options});
}

absl::Status CopyReadChunk(
    ReadChunk::Impl& chunk, IndexTransform<> chunk_transform,
    const DataTypeConversionLookupResult& chunk_conversion,
    NormalizedTransformedArray<void, dynamic_rank, view> target) {
  DefaultNDIterableArena arena;

  TENSORSTORE_ASSIGN_OR_RETURN(
      auto target_iterable,
      GetNormalizedTransformedArrayNDIterable(UnownedToShared(target), arena));

  LockCollection lock_collection;
  TENSORSTORE_ASSIGN_OR_RETURN(auto guard, LockChunks(lock_collection, chunk));

  TENSORSTORE_ASSIGN_OR_RETURN(
      auto source_iterable,
      chunk(ReadChunk::BeginRead{}, std::move(chunk_transform), arena));

  source_iterable = GetConvertedInputNDIterable(
      std::move(source_iterable), target_iterable->dtype(), chunk_conversion);

  // Copy the chunk to the relevant portion of the target array.
  NDIterableCopier copier(*source_iterable, *target_iterable, target.shape(),
                          arena);
  return copier.Copy();
}

absl::Status CopyReadChunk(
    ReadChunk::Impl& chunk, IndexTransform<> chunk_transform,
    NormalizedTransformedArray<void, dynamic_rank, view> target) {
  auto converter =
      internal::GetDataTypeConverter(target.dtype(), target.dtype());
  return CopyReadChunk(chunk, std::move(chunk_transform), converter,
                       std::move(target));
}

Result<ChunkLayout> GetChunkLayout(const Driver::Handle& handle) {
  assert(handle.driver);
  return handle.driver->GetChunkLayout(handle.transform);
}

Result<CodecSpec::Ptr> GetCodec(const Driver::Handle& handle) {
  assert(handle.driver);
  return handle.driver->GetCodec();
}

Result<Schema> GetSchema(const Driver::Handle& handle) {
  Schema schema;
  TENSORSTORE_RETURN_IF_ERROR(schema.Set(handle.driver->dtype()));
  TENSORSTORE_RETURN_IF_ERROR(schema.Set(handle.transform.domain()));
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto chunk_layout, GetChunkLayout(handle));
    TENSORSTORE_RETURN_IF_ERROR(schema.Set(std::move(chunk_layout)));
  }
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto codec, GetCodec(handle));
    TENSORSTORE_RETURN_IF_ERROR(schema.Set(std::move(codec)));
  }
  {
    TENSORSTORE_ASSIGN_OR_RETURN(auto fill_value, GetFillValue(handle));
    TENSORSTORE_RETURN_IF_ERROR(
        schema.Set(Schema::FillValue(std::move(fill_value))));
  }
  return schema;
}

}  // namespace internal
}  // namespace tensorstore
