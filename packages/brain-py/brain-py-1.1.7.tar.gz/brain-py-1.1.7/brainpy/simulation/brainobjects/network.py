# -*- coding: utf-8 -*-

from brainpy.simulation.brainobjects.base import Container

__all__ = [
  'Network'
]


class Network(Container):
  """Base class to model network objects, an alias of Container.

  Network instantiates a network, which is aimed to load
  neurons, synapses, and other brain objects.

  Parameters
  ----------
  name : str, Optional
    The network name.
  monitors : optional, list of str, tuple of str
    The items to monitor.
  ds_tuple : 
    A list/tuple container of dynamical system.
  ds_dict : 
    A dict container of dynamical system. 
  """

  def __init__(self, *ds_tuple, monitors=None, name=None, **ds_dict):
    super(Network, self).__init__(*ds_tuple, name=name, monitors=monitors, **ds_dict)
