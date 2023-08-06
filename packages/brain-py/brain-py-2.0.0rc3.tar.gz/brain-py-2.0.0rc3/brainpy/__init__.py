# -*- coding: utf-8 -*-

__version__ = "2.0.0rc3"


# "base" module
from . import base
from .base.base import Base
from .base.collector import Collector, TensorCollector


# "math" module
from . import math


# "integrators" module
from . import integrators
from .integrators import ode
from .integrators import sde
from .integrators.ode import odeint
from .integrators.ode import set_default_odeint
from .integrators.ode import get_default_odeint
from .integrators.sde import sdeint
from .integrators.sde import set_default_sdeint
from .integrators.sde import get_default_sdeint


# "simulation" module
from . import simulation
from .simulation.brainobjects import *
from .simulation.monitor import *
from .simulation.runner import *
from .simulation import brainobjects
from .simulation import models
from .simulation import connect
conn = connect
from .simulation import inputs
from .simulation import measure

# "training" module
from . import training
from .training import layers, initialize
init = initialize

# "analysis" module
from . import analysis


# "visualization" module
from . import visualization as visualize


# other modules
from . import errors
from . import running
from . import tools
