# -*- coding: utf-8 -*-


class JaxTracerError(Exception):
  def __init__(self):
    super(JaxTracerError, self).__init__(
      'There is an unexpected tracer. \n\n'
      'In BrainPy, all the dynamically changed variables must be provided '
      'into the "dyn_vars" when calling the transformation functions, '
      'like "jit()", "vmap()", "grad()", "make_loop()", etc. \n\n'
      'We found there are changed variables which are not wrapped into "dyn_vars". Please check!'
    )


class RunningError(Exception):
  """The error occurred in the running function."""
  pass


class BrainPyError(Exception):
  """General BrainPy error."""
  pass


class IntegratorError(Exception):
  pass


class DiffEqError(Exception):
  """The differential equation definition error.
  """
  pass


class CodeError(Exception):
  """Code definition error.
  """
  pass


class AnalyzerError(Exception):
  """Differential equation analyzer error.
  """


class PackageMissingError(Exception):
  """The package missing error.
  """
  pass


class BackendNotInstalled(Exception):
  def __init__(self, backend):
    super(BackendNotInstalled, self).__init__(
      '"{bk}" must be installed when the user wants to use {bk} backend. \n'
      'Please install {bk} through "pip install {bk}" '
      'or "conda install {bk}".'.format(bk=backend))


class UniqueNameError(Exception):
  def __init__(self, *args):
    super(UniqueNameError, self).__init__(*args)


class UnsupportedError(Exception):
  pass


class NoLongerSupportError(Exception):
  pass

