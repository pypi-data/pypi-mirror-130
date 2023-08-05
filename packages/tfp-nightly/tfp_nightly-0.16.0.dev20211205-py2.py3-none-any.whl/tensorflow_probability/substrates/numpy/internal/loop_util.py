# Copyright 2021 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Utilities for looping."""

import numpy as np
from tensorflow_probability.python.internal.backend.numpy.compat import v1 as tf1
from tensorflow_probability.python.internal.backend.numpy.compat import v2 as tf

from tensorflow_probability.substrates.numpy.internal import prefer_static as ps
from tensorflow_probability.substrates.numpy.internal import tensorshape_util
from tensorflow_probability.python.internal.backend.numpy import private as control_flow_util  # pylint: disable=g-direct-tensorflow-import

JAX_MODE = False


__all__ = [
    'smart_for_loop',
    'trace_scan'
]


def _initialize_arrays(initial_values,
                       num_steps):
  """Construct a structure of `TraceArray`s from initial values."""
  trace_arrays = tf.nest.map_structure(
      lambda t: tf.TensorArray(  # pylint: disable=g-long-lambda
          dtype=t.dtype,
          size=num_steps,  # Initial size.
          clear_after_read=False,  # Allow reading->tiling final value.
          element_shape=t.shape),
      initial_values)
  return tf.nest.map_structure(
      lambda ta, t: ta.write(0, t), trace_arrays, initial_values)


def smart_for_loop(loop_num_iter, body_fn, initial_loop_vars,
                   parallel_iterations=10, unroll_threshold=1, name=None):
  """Construct a for loop, preferring a python loop if `n` is statically known.

  Given `loop_num_iter` and `body_fn`, return an op corresponding to executing
  `body_fn` `loop_num_iter` times, feeding previous outputs of `body_fn` into
  the next iteration.

  If `loop_num_iter` is statically known, the op is constructed via python for
  loop, and otherwise a `tf.while_loop` is used.

  Args:
    loop_num_iter: `Integer` `Tensor` representing the number of loop
      iterations.
    body_fn: Callable to be executed `loop_num_iter` times.
    initial_loop_vars: Listlike object of `Tensors` to be passed in to
      `body_fn`'s first execution.
    parallel_iterations: The number of iterations allowed to run in parallel.
      It must be a positive integer. See `tf.while_loop` for more details.
      Default value: `10`.
    unroll_threshold: Integer denoting the maximum number of iterations to
      unroll, if possible. If `loop_num_iter > unroll_threshold` a
      `tf.while_loop` will always be used, even if `loop_num_iter` is
      statically known.
      Default value: `1`.
    name: Python `str` name prefixed to Ops created by this function.
      Default value: `None` (i.e., "smart_for_loop").
  Returns:
    result: `Tensor` representing applying `body_fn` iteratively `n` times.
  """
  with tf.name_scope(name or 'smart_for_loop'):
    loop_num_iter_ = tf.get_static_value(loop_num_iter)
    if (loop_num_iter_ is None
        or tf.executing_eagerly()
        # large values for loop_num_iter_ will cause ridiculously slow
        # graph compilation time (GitHub issue #1033)
        or loop_num_iter_ > unroll_threshold
        or control_flow_util.GraphOrParentsInXlaContext(
            tf1.get_default_graph())):
      # Cast to int32 to run the comparison against i in host memory,
      # where while/LoopCond needs it.
      loop_num_iter = tf.cast(loop_num_iter, dtype=tf.int32)
      return tf.while_loop(
          cond=lambda i, *args: i < loop_num_iter,
          body=lambda i, *args: [i + 1] + list(body_fn(*args)),
          loop_vars=[np.int32(0)] + initial_loop_vars,
          parallel_iterations=parallel_iterations
      )[1:]
    result = initial_loop_vars
    for _ in range(loop_num_iter_):
      result = body_fn(*result)
    return result


def trace_scan(loop_fn,
               initial_state,
               elems,
               trace_fn,
               trace_criterion_fn=None,
               static_trace_allocation_size=None,
               condition_fn=None,
               parallel_iterations=10,
               name=None):
  """A simplified version of `tf.scan` that has configurable tracing.

  This function repeatedly calls `loop_fn(state, elem)`, where `state` is the
  `initial_state` during the first iteration, and the return value of `loop_fn`
  for every iteration thereafter. `elem` is a slice of `elements` along the
  first dimension, accessed in order. Additionally, it calls `trace_fn` on the
  return value of `loop_fn`. The `Tensor`s in return values of `trace_fn` are
  stacked and returned from this function, such that the first dimension of
  those `Tensor`s matches the size of `elems`.

  Args:
    loop_fn: A callable that takes in a `Tensor` or a nested collection of
      `Tensor`s with the same structure as `initial_state`, a slice of `elems`
      and returns the same structure as `initial_state`.
    initial_state: A `Tensor` or a nested collection of `Tensor`s passed to
      `loop_fn` in the first iteration.
    elems: A `Tensor` that is split along the first dimension and each element
      of which is passed to `loop_fn`.
    trace_fn: A callable that takes in the return value of `loop_fn` and returns
      a `Tensor` or a nested collection of `Tensor`s.
    trace_criterion_fn: Optional callable that takes in the return value of
      `loop_fn` and returns a boolean `Tensor` indicating whether to trace it.
      If `None`, all steps are traced.
      Default value: `None`.
    static_trace_allocation_size: Optional Python `int` size of trace to
      allocate statically. This should be an upper bound on the number of steps
      traced and is used only when the length cannot be
      statically inferred (for example, if a `trace_criterion_fn` is specified).
      It is primarily intended for contexts where static shapes are required,
      such as in XLA-compiled code.
      Default value: `None`.
    condition_fn: Python `callable` additional loop termination condition, with
     signature `should_continue = condition_fn(step, state, num_traced, trace)`;
     returning `False` will terminate early and not scan over all of `elems`.
     Default value: `None`, which means no additional termination condition.
    parallel_iterations: Passed to the internal `tf.while_loop`.
    name: Name scope used in this function. Default: 'trace_scan'.

  Returns:
    final_state: The final return value of `loop_fn`.
    trace: The same structure as the return value of `trace_fn`, but with each
      `Tensor` being a stack of the corresponding `Tensors` in the return value
      of `trace_fn` for each slice of `elems`.
  """
  with tf.name_scope(name or 'trace_scan'), tf1.variable_scope(
      tf1.get_variable_scope()) as vs:
    if vs.caching_device is None and not tf.executing_eagerly():
      vs.set_caching_device(lambda op: op.device)

    initial_state = tf.nest.map_structure(
        lambda x: tf.convert_to_tensor(x, name='initial_state'),
        initial_state, expand_composites=True)
    elems = tf.convert_to_tensor(elems, name='elems')

    length = ps.size0(elems)

    # This is an TensorArray in part because of XLA, which had trouble with
    # non-statically known indices. I.e. elems[i] errored, but
    # elems_array.read(i) worked.
    elems_array = tf.TensorArray(
        elems.dtype, size=length, element_shape=elems.shape[1:])
    elems_array = elems_array.unstack(elems)

    # Initialize trace arrays.
    if trace_criterion_fn is None and condition_fn is None:
      dynamic_size, initial_size = tf.is_tensor(length), length
    elif static_trace_allocation_size is not None:
      dynamic_size, initial_size = False, static_trace_allocation_size
    elif JAX_MODE or (not tf.executing_eagerly() and
                      control_flow_util.GraphOrParentsInXlaContext(
                          tf1.get_default_graph())):
      dynamic_size, initial_size = False, length
    else:
      dynamic_size, initial_size = True, 0
    initial_trace = trace_fn(initial_state)
    flat_initial_trace = tf.nest.flatten(initial_trace, expand_composites=True)
    trace_arrays = []
    for trace_elt in flat_initial_trace:
      trace_arrays.append(
          tf.TensorArray(
              trace_elt.dtype,
              size=initial_size,
              dynamic_size=dynamic_size,
              element_shape=trace_elt.shape))

    # Helper for writing a (structured) state to (structured) arrays.
    def trace_one_step(num_steps_traced, trace_arrays, state):
      return [ta.write(num_steps_traced, x) for ta, x in
              zip(trace_arrays,
                  tf.nest.flatten(trace_fn(state), expand_composites=True))]

    def _body(i, state, num_steps_traced, trace_arrays):
      elem = elems_array.read(i)
      state = loop_fn(state, elem)

      trace_arrays, num_steps_traced = ps.cond(
          trace_criterion_fn(state) if trace_criterion_fn else True,
          lambda: (trace_one_step(num_steps_traced, trace_arrays, state),  # pylint: disable=g-long-lambda
                   num_steps_traced + 1),
          lambda: (trace_arrays, num_steps_traced))

      return i + 1, state, num_steps_traced, trace_arrays

    if condition_fn is None:
      cond = lambda i, *_: i < length
    else:
      cond = lambda i, *rest: (i < length) & condition_fn(i, *rest)

    _, final_state, _, trace_arrays = tf.while_loop(
        cond=cond,
        body=_body,
        loop_vars=(0, initial_state, 0, trace_arrays),
        parallel_iterations=parallel_iterations)

    # unflatten
    stacked_trace = tf.nest.pack_sequence_as(
        initial_trace, [ta.stack() for ta in trace_arrays],
        expand_composites=True)

    # Restore the static length if we know it.
    static_length = tf.TensorShape(None if dynamic_size else initial_size)

    def _merge_static_length(x):
      tensorshape_util.set_shape(x, static_length.concatenate(x.shape[1:]))
      return x

    stacked_trace = tf.nest.map_structure(
        _merge_static_length, stacked_trace, expand_composites=True)
    return final_state, stacked_trace


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# This file is auto-generated by substrates/meta/rewrite.py
# It will be surfaced by the build system as a symlink at:
#   `tensorflow_probability/substrates/numpy/internal/loop_util.py`
# For more info, see substrate_runfiles_symlinks in build_defs.bzl
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
