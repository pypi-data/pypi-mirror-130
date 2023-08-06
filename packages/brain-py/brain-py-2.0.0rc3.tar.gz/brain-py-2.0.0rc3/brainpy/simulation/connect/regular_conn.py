# -*- coding: utf-8 -*-

import logging

import numpy as np

from brainpy import errors, tools
from scipy.sparse import csr_matrix
from .base import *

logger = logging.getLogger('brainpy.simulation.connect')

__all__ = [
  'One2One', 'one2one',
  'All2All', 'all2all',
  'GridFour', 'grid_four',
  'GridEight', 'grid_eight',
  'GridN',
]


class One2One(TwoEndConnector):
  """Connect two neuron groups one by one. This means
  The two neuron groups should have the same size.
  """

  def __call__(self, pre_size, post_size):
    self._reset_conn(pre_size=pre_size, post_size=post_size)

    if self.pre_num != self.post_num:
      raise errors.ConnectorError(f'One2One connection must be defined in two groups with the '
                                  f'same size, but we got {self.pre_num} != {self.post_num}.')

    mat = np.zeros((self.pre_num, self.post_num), dtype=MAT_DTYPE)
    np.fill_diagonal(mat, True)

    self.data = csr_matrix(mat)

    return self

one2one = One2One()


class All2All(TwoEndConnector):
  """Connect each neuron in first group to all neurons in the
  post-synaptic neuron groups. It means this kind of conn
  will create (num_pre x num_post) synapses.
  """

  def __init__(self, include_self=True):
    self.include_self = include_self
    super(All2All, self).__init__()

  def __call__(self, pre_size, post_size):
    self._reset_conn(pre_size=pre_size, post_size=post_size)

    mat = np.ones((self.pre_num, self.post_num), dtype=MAT_DTYPE)
    if not self.include_self: np.fill_diagonal(mat, False)

    self.data = csr_matrix(mat)

    return self

all2all = All2All(include_self=True)


@tools.numba_jit
def _grid_four(height, width, row, include_self):
  conn_i = []
  conn_j = []

  for col in range(width):
    i_index = (row * width) + col
    if 0 <= row - 1 < height:
      j_index = ((row - 1) * width) + col
      conn_i.append(i_index)
      conn_j.append(j_index)
    if 0 <= row + 1 < height:
      j_index = ((row + 1) * width) + col
      conn_i.append(i_index)
      conn_j.append(j_index)
    if 0 <= col - 1 < width:
      j_index = (row * width) + col - 1
      conn_i.append(i_index)
      conn_j.append(j_index)
    if 0 <= col + 1 < width:
      j_index = (row * width) + col + 1
      conn_i.append(i_index)
      conn_j.append(j_index)
    if include_self:
      conn_i.append(i_index)
      conn_j.append(i_index)
  return conn_i, conn_j


class GridFour(OneEndConnector):
  """The nearest four neighbors conn method."""

  def __init__(self, include_self=False):
    super(GridFour, self).__init__()
    self.include_self = include_self

  def __call__(self, pre_size, post_size=None):
    self._reset_conn(pre_size=pre_size, post_size=post_size)

    assert self.pre_size == self.post_size
    if len(self.pre_size) == 1:
      height, width = self.pre_size[0], 1
    elif len(self.pre_size) == 2:
      height, width = self.pre_size
    else:
      raise errors.BrainPyError('Currently only support two-dimensional geometry.')

    conn_i = []
    conn_j = []
    for row in range(height):
      a = _grid_four(height, width, row, include_self=self.include_self)
      conn_i.extend(a[0])
      conn_j.extend(a[1])
    pre_ids = np.asarray(conn_i, dtype=IDX_DTYPE)
    post_ids = np.asarray(conn_j, dtype=IDX_DTYPE)

    self.data = csr_matrix((np.ones_like(pre_ids, np.bool_), (pre_ids, post_ids)), shape=(pre_size, post_size))

    return self

grid_four = GridFour()


@tools.numba_jit
def _grid_n(height, width, row, n, include_self):
  conn_i = []
  conn_j = []
  for col in range(width):
    i_index = (row * width) + col
    for row_diff in range(-n, n + 1):
      for col_diff in range(-n, n + 1):
        if (not include_self) and (row_diff == col_diff == 0):
          continue
        if 0 <= row + row_diff < height and 0 <= col + col_diff < width:
          j_index = ((row + row_diff) * width) + col + col_diff
          conn_i.append(i_index)
          conn_j.append(j_index)
  return conn_i, conn_j


class GridN(OneEndConnector):
  """The nearest (2*N+1) * (2*N+1) neighbors conn method.

  Parameters
  ----------
  N : int
      Extend of the conn scope. For example:
      When N=1,
          [x x x]
          [x I x]
          [x x x]
      When N=2,
          [x x x x x]
          [x x x x x]
          [x x I x x]
          [x x x x x]
          [x x x x x]
  include_self : bool
      Whether create (i, i) conn ?
  """

  def __init__(self, N=1, include_self=False):
    super(GridN, self).__init__()
    self.N = N
    self.include_self = include_self

  def __call__(self, pre_size, post_size=None):
    self._reset_conn(pre_size=pre_size, post_size=post_size)

    try:
      assert self.pre_size == self.post_size
    except AssertionError:
      raise errors.BrainPyError(
        f'The shape of pre-synaptic group should be the same with the post group. '
        f'But we got {self.pre_size} != {self.post_size}.')

    if len(self.pre_size) == 1:
      height, width = self.pre_size[0], 1
    elif len(self.pre_size) == 2:
      height, width = self.pre_size
    else:
      raise errors.BrainPyError('Currently only support two-dimensional geometry.')

    conn_i = []
    conn_j = []
    for row in range(height):
      res = _grid_n(height=height, width=width, row=row,
                    n=self.N, include_self=self.include_self)
      conn_i.extend(res[0])
      conn_j.extend(res[1])
    pre_ids = np.asarray(conn_i, dtype=IDX_DTYPE)
    post_ids = np.asarray(conn_j, dtype=IDX_DTYPE)

    self.data = csr_matrix((np.ones_like(pre_ids, np.bool_), (pre_ids, post_ids)), shape=(pre_size, post_size))

    return self


class GridEight(GridN):
  """The nearest eight neighbors conn method."""

  def __init__(self, include_self=False):
    super(GridEight, self).__init__(N=1, include_self=include_self)


grid_eight = GridEight()
