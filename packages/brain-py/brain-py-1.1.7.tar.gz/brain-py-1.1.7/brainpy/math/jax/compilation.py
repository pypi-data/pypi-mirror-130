# -*- coding: utf-8 -*-

"""
The JIT compilation tools for JAX backend.

1. Just-In-Time compilation is implemented by the 'jit()' function

"""

import functools
import logging

import jax

try:
  from jax.errors import UnexpectedTracerError
except ImportError:
  from jax.core import UnexpectedTracerError

from brainpy import errors
from brainpy.base.base import Base
from brainpy.base.collector import TensorCollector
from brainpy.math.jax.jaxarray import JaxArray
from brainpy.tools.codes import change_func_name

__all__ = [
  'jit',
]

logger = logging.getLogger('brainpy.math.jax.compilation')


def _make_jit(func, vars, static_argnames=None, device=None, f_name=None):
  @functools.partial(jax.jit, static_argnames=static_argnames, device=device)
  def jitted_func(variable_data, *args, **kwargs):
    vars.assign(variable_data)
    out = func(*args, **kwargs)
    changes = vars.dict()
    return out, changes

  def call(*args, **kwargs):
    variable_data = vars.dict()
    try:
      out, changes = jitted_func(variable_data, *args, **kwargs)
    except UnexpectedTracerError as e:
      vars.assign(variable_data)
      raise errors.JaxTracerError() from e
    vars.assign(changes)
    return out

  return change_func_name(name=f_name, f=call) if f_name else call


def jit(obj_or_func, dyn_vars=None, static_argnames=None, device=None, **kwargs):
  """JIT (Just-In-Time) Compilation for JAX backend.

  This function has the same ability to Just-In-Time compile a pure function,
  but it can also JIT compile a :py:class:`brainpy.DynamicalSystem`, or a
  :py:class:`brainpy.Base` object, or a bounded method of a
  :py:class:`brainpy.Base` object.

  If you are using "numpy", please refer to the JIT compilation
  in NumPy backend `bp.math.numpy.jit() <brainpy.math.numpy.jit.rst>`_.

  Notes
  -----

  There are several notes:

  1. Avoid using scalar in Variable, TrainVar, etc.
  2. ``jit`` compilation in ``brainpy.math.jax`` does not support `static_argnums`.
     Instead, users should use `static_argnames`, and call the jitted function with
     keywords like ``jitted_func(arg1=var1, arg2=var2)``.

  Examples
  --------

  You can JIT a :py:class:`brainpy.DynamicalSystem`

  >>> import brainpy as bp
  >>>
  >>> class LIF(bp.NeuGroup):
  >>>   pass
  >>> lif = bp.math.jit(LIF(10))

  You can JIT a :py:class:`brainpy.Base` object with ``__call__()`` implementation.

  >>> mlp = bp.layers.GRU(100, 200)
  >>> jit_mlp = bp.math.jit(mlp)

  You can also JIT a bounded method of a :py:class:`brainpy.Base` object.

  >>> class Hello(bp.Base):
  >>>   def __init__(self):
  >>>     super(Hello, self).__init__()
  >>>     self.a = bp.math.Variable(bp.math.array(10.))
  >>>     self.b = bp.math.Variable(bp.math.array(2.))
  >>>   def transform(self):
  >>>     return self.a ** self.b
  >>>
  >>> test = Hello()
  >>> bp.math.jit(test.transform)

  Further, you can JIT a normal function, just used like in JAX.

  >>> @bp.math.jit
  >>> def selu(x, alpha=1.67, lmbda=1.05):
  >>>   return lmbda * bp.math.where(x > 0, x, alpha * bp.math.exp(x) - alpha)


  Parameters
  ----------
  obj_or_func : Base, function
    The instance of Base or a function.
  dyn_vars : optional, dict, tuple, list, JaxArray
    These variables will be changed in the function, or needed in the computation.
  static_argnames : optional, str, list, tuple, dict
    An optional string or collection of strings specifying which named arguments to treat
    as static (compile-time constant). See the comment on ``static_argnums`` for details.
    If not provided but ``static_argnums`` is set, the default is based on calling
    ``inspect.signature(fun)`` to find corresponding named arguments.
  device: optional, Any
    This is an experimental feature and the API is likely to change.
    Optional, the Device the jitted function will run on. (Available devices
    can be retrieved via :py:func:`jax.devices`.) The default is inherited
    from XLA's DeviceAssignment logic and is usually to use
    ``jax.devices()[0]``.

  Returns
  -------
  ds_of_func :
    A wrapped version of Base object or function, set up for just-in-time compilation.
  """
  from brainpy.simulation.brainobjects.base import DynamicalSystem

  if isinstance(obj_or_func, DynamicalSystem):
    if len(obj_or_func.steps):  # DynamicalSystem has step functions

      # dynamical variables
      dyn_vars = (dyn_vars or obj_or_func.vars().unique())
      if isinstance(dyn_vars, JaxArray):
        dyn_vars = TensorCollector({'_': dyn_vars})
      elif isinstance(dyn_vars, dict):
        dyn_vars = TensorCollector(dyn_vars)
      elif isinstance(dyn_vars, (tuple, list)):
        dyn_vars = TensorCollector({f'_v{i}': v for i, v in enumerate(dyn_vars)})
      else:
        raise ValueError

      # static arguments by name
      if static_argnames is None:
        static_argnames = {key: None for key in obj_or_func.steps.keys()}
      elif isinstance(static_argnames, str):
        static_argnames = {key: (static_argnames,) for key in obj_or_func.steps.keys()}
      elif isinstance(static_argnames, (tuple, list)) and isinstance(static_argnames[0], str):
        static_argnames = {key: static_argnames for key in obj_or_func.steps.keys()}
      assert isinstance(static_argnames, dict)

      # jit functions
      for key in list(obj_or_func.steps.keys()):
        jitted_func = _make_jit(vars=dyn_vars,
                                func=obj_or_func.steps[key],
                                static_argnames=static_argnames[key],
                                device=device,
                                f_name=key)
        obj_or_func.steps.replace(key, jitted_func)
      return obj_or_func

  if callable(obj_or_func):
    if dyn_vars is not None:
      if isinstance(dyn_vars, JaxArray):
        dyn_vars = TensorCollector({'_': dyn_vars})
      elif isinstance(dyn_vars, dict):
        dyn_vars = TensorCollector(dyn_vars)
      elif isinstance(dyn_vars, (tuple, list)):
        dyn_vars = TensorCollector({f'_v{i}': v for i, v in enumerate(dyn_vars)})
      else:
        raise ValueError
    elif isinstance(obj_or_func, Base):
      dyn_vars = obj_or_func.vars().unique()
    elif hasattr(obj_or_func, '__self__') and isinstance(obj_or_func.__self__, Base):
      dyn_vars = obj_or_func.__self__.vars().unique()
    else:
      dyn_vars = TensorCollector()

    if len(dyn_vars) == 0:  # pure function
      return jax.jit(obj_or_func,
                     static_argnames=static_argnames,
                     device=device)

    else:  # Base object which implements __call__, or bounded method of Base object
      return _make_jit(vars=dyn_vars,
                       func=obj_or_func,
                       static_argnames=static_argnames,
                       device=device)

  else:
    raise errors.BrainPyError(f'Only support instance of {Base.__name__}, or a callable '
                              f'function, but we got {type(obj_or_func)}.')
