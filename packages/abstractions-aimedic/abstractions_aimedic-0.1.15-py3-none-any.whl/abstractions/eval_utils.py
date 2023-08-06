from tensorflow.keras.utils import unpack_x_y_sample_weight
import tensorflow as tf
from tensorflow.keras import backend


def make_test_function(force=False):
    def _minimum_control_deps(outputs):
        """Returns the minimum control dependencies to ensure step succeeded."""
        if tf.executing_eagerly():
            return []  # Control dependencies not needed.
        outputs = tf.nest.flatten(outputs, expand_composites=True)
        for out in outputs:
            # Variables can't be control dependencies.
            if not isinstance(out, tf.Variable):
                return [out]  # Return first Tensor or Op from outputs.
        return []  # No viable Tensor or Op to use for control deps.

    def reduce_per_replica(values, strategy, reduction='first'):
        """Reduce PerReplica objects.
        Args:
          values: Structure of `PerReplica` objects or `Tensor`s. `Tensor`s are
            returned as-is.
          strategy: `tf.distribute.Strategy` object.
          reduction: One of 'first', 'concat'.
        Returns:
          Structure of `Tensor`s.
        """

        def _reduce(v):
            """Reduce a single `PerReplica` object."""
            if reduction == 'concat' and _collective_all_reduce_multi_worker(strategy):
                return _multi_worker_concat(v, strategy)
            if not _is_per_replica_instance(v):
                return v
            elif reduction == 'first':
                return strategy.unwrap(v)[0]
            elif reduction == 'concat':
                if _is_tpu_multi_host(strategy):
                    return _tpu_multi_host_concat(v, strategy)
                else:
                    return concat(strategy.unwrap(v))
            else:
                raise ValueError('`reduction` must be "first" or "concat". Received: '
                                 f'reduction={reduction}.')

        return tf.nest.map_structure(_reduce, values)

    def _collective_all_reduce_multi_worker(strategy):
        return (isinstance(strategy,
                           tf.distribute.MultiWorkerMirroredStrategy)
                ) and strategy.extended._in_multi_worker_mode()  # pylint: disable=protected-access

    def _multi_worker_concat(v, strategy):
        """Order PerReplica objects for CollectiveAllReduceStrategy and concat."""
        replicas = strategy.gather(v, axis=0)
        # v might not have the same shape on different replicas
        if _is_per_replica_instance(v):
            shapes = tf.concat([
                tf.expand_dims(tf.shape(single_value)[0], axis=0)
                for single_value in v.values
            ], axis=0)
            all_shapes = strategy.gather(shapes, axis=0)
        else:
            # v is a tensor. This may happen when, say, we have 2x1 multi-worker.
            all_shapes = strategy.gather(
                tf.expand_dims(tf.shape(v)[0], axis=0), axis=0)

        replicas = tf.split(
            replicas,
            num_or_size_splits=all_shapes,
            num=strategy.num_replicas_in_sync)
        ordered_replicas = []
        num_replicas_per_worker = len(strategy.extended.worker_devices)
        for replica_id in range(num_replicas_per_worker):
            ordered_replicas += replicas[replica_id::num_replicas_per_worker]
        return concat(ordered_replicas)

    def _is_per_replica_instance(obj):
        return (isinstance(obj, tf.distribute.DistributedValues) and
                isinstance(obj, tf.__internal__.CompositeTensor))

    def _is_tpu_multi_host(strategy):
        return (backend.is_tpu_strategy(strategy) and
                strategy.extended.num_hosts > 1)

    def concat(tensors, axis=0):
        """Concats `tensor`s along `axis`."""
        if isinstance(tensors[0], tf.SparseTensor):
            return tf.sparse.concat(axis=axis, sp_inputs=tensors)
        return tf.concat(tensors, axis=axis)

    def _tpu_multi_host_concat(v, strategy):
        """Correctly order TPU PerReplica objects."""
        replicas = strategy.unwrap(v)
        # When distributed datasets are created from Tensors / NumPy,
        # TPUStrategy.experimental_distribute_dataset shards data in
        # (Replica, Host) order, and TPUStrategy.unwrap returns it in
        # (Host, Replica) order.
        # TODO(b/150317897): Figure out long-term plan here.
        num_replicas_per_host = strategy.extended.num_replicas_per_host
        ordered_replicas = []
        for replica_id in range(num_replicas_per_host):
            ordered_replicas += replicas[replica_id::num_replicas_per_host]
        return concat(ordered_replicas)

    def test_step(data, model):
        x, y, sample_weight = unpack_x_y_sample_weight(data)

        y_pred = model(x, training=False)
        # Updates stateful loss metrics.
        model.compiled_loss(
            y, y_pred, sample_weight, regularization_losses=model.losses)
        model.compiled_metrics.update_state(y, y_pred, sample_weight)
        # Collect metrics to return
        return_metrics = {}
        for metric in model.metrics:
            result = metric.result()
            if isinstance(result, dict):
                return_metrics.update(result)
            else:
                return_metrics[metric.name] = result
        return_metrics['pred'] = y_pred
        return return_metrics

    self = model

    if self.test_function is not None and not force:
        return self.test_function

    def step_function(model, iterator):
        """Runs a single evaluation step."""

        def run_step(data):
            outputs = test_step(data, model)
            # Ensure counter is updated only if `test_step` succeeds.
            with tf.control_dependencies(_minimum_control_deps(outputs)):
                model._test_counter.assign_add(1)  # pylint: disable=protected-access
            return outputs

        data = next(iterator)
        outputs = model.distribute_strategy.run(run_step, args=(data,))
        pred = outputs.pop('pred')
        outputs = reduce_per_replica(
            outputs, self.distribute_strategy, reduction='first')
        return outputs, pred

    if (self._steps_per_execution is None or
            self._steps_per_execution.numpy().item() == 1):

        def test_function(iterator):
            """Runs an evaluation execution with one step."""
            outputs, pred = step_function(self, iterator)
            outputs['pred'] = pred
            return outputs

    else:

        def test_function(iterator):
            """Runs an evaluation execution with multiple steps."""
            preds = list()
            for _ in tf.range(self._steps_per_execution):
                outputs, pred = step_function(self, iterator)
                preds.extend(pred)
            outputs['pred'] = preds
            return outputs

    if not self.run_eagerly:
        test_function = tf.function(
            test_function, experimental_relax_shapes=True)

    self.test_function = test_function

    if self._cluster_coordinator:
        self.test_function = lambda iterator: self._cluster_coordinator.schedule(  # pylint: disable=g-long-lambda
            test_function, args=(iterator,))

    return self.test_function


def wrap_make_test_function(model):
    """After calling this on your model, you will have ``{'loss': [], 'metric1': [], ..., 'pred': []}`` as the
    output of the ``model.evaluate`` method."""

    setattr(model, 'make_test_function', make_test_function)
