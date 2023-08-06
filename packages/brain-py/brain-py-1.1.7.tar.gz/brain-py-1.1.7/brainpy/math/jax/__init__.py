# -*- coding: utf-8 -*-

# necessity to wrap the jax.numpy.ndarray:
# 1. for parameters and variables which want to
#    modify in the JIT mode, this wrapper is necessary.
#    Because, directly change the value in the "self.xx"
#    cannot work.
# 2. In JAX, ndarray is immutable. This wrapper make
#    the index update is the same way with the numpy
#

# data structure
from .jaxarray import *

# functions/operations
from .ops import *
from .operators import *
from . import fft
from . import linalg
from . import random
from . import activations
from .activations import *
from . import losses
from . import optimizers

# transformations
from .autograd import *
from .controls import *
from .compilation import *
from .parallels import *

# others
from .function import *
