# -*- coding: utf-8 -*-

import numpy as np
from brainpy import errors, tools
from .base import *

__all__ = [
  'One2One', 'one2one',
  'All2All', 'all2all',
  'GridFour', 'grid_four',
  'GridEight', 'grid_eight',
  'GridN',
]


class One2One(TwoEndConnector):
  """
  Connect two neuron groups one by one. This means
  The two neuron groups should have the same size.
  """

  def __init__(self):
    super(One2One, self).__init__()

  def require(self, *structures):
    try:
      assert self.pre_num == self.post_num
    except AssertionError:
      raise errors.BrainPyError(f'One2One connection must be defined in two groups with the '
                                f'same size, but we got {self.pre_num} != {self.post_num}.')

    type_to_provide = self.check(structures)

    if type_to_provide == PROVIDE_MAT:
      mat = np.zeros((self.pre_num, self.post_num), dtype=np.bool_)
      np.fill_diagonal(mat, True)
      return self.returns(mat=mat)

    elif type_to_provide == PROVIDE_IJ:
      pre_ids = np.arange(self.pre_num, dtype=np.int_)
      post_ids = np.arange(self.pre_num, dtype=np.int_)
      return self.returns(ij=(pre_ids, post_ids))

    else:
      raise ValueError


one2one = One2One()


class All2All(TwoEndConnector):
  """Connect each neuron in first group to all neurons in the
  post-synaptic neuron groups. It means this kind of conn
  will create (num_pre x num_post) synapses.
  """

  def __init__(self, include_self=True):
    self.include_self = include_self
    super(All2All, self).__init__()

  def require(self, *structures):
    type_to_provide = self.check(structures)

    if type_to_provide == PROVIDE_MAT:
      mat = np.ones((self.pre_num, self.post_num), dtype=bool)
      if not self.include_self: np.fill_diagonal(mat, False)
      return self.returns(mat=mat)

    elif type_to_provide == PROVIDE_IJ:
      mat = np.ones((self.pre_num, self.post_num), dtype=bool)
      if not self.include_self: np.fill_diagonal(mat, False)
      pre_ids, post_ids = np.where(mat)
      del mat
      pre_ids = np.asarray(pre_ids, dtype=np.int_)
      post_ids = np.asarray(post_ids, dtype=np.int_)
      return self.returns(ij=(pre_ids, post_ids))

    else:
      raise ValueError


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

  def require(self, *structures):
    type_to_provide = self.check(structures)

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
    pre_ids = np.asarray(conn_i, dtype=np.int_)
    post_ids = np.asarray(conn_j, dtype=np.int_)

    if type_to_provide == PROVIDE_MAT:
      mat = np.zeros((self.pre_num, self.post_num), dtype=np.bool_)
      mat[pre_ids, post_ids] = True
      return self.returns(mat=mat, ij=(pre_ids, post_ids))

    elif type_to_provide == PROVIDE_IJ:
      return self.returns(ij=(pre_ids, post_ids))

    else:
      raise ValueError


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



  def require(self, *structures):
    type_to_provide = self.check(structures)

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
    pre_ids = np.asarray(conn_i, dtype=np.int_)
    post_ids = np.asarray(conn_j, dtype=np.int_)

    if type_to_provide == PROVIDE_MAT:
      mat = np.zeros((self.pre_num, self.post_num), dtype=np.bool_)
      mat[pre_ids, post_ids] = True
      return self.returns(mat=mat, ij=(pre_ids, post_ids))

    elif type_to_provide == PROVIDE_IJ:
      return self.returns(ij=(pre_ids, post_ids))

    else:
      raise ValueError


class GridEight(GridN):
  """The nearest eight neighbors conn method."""

  def __init__(self, include_self=False):
    super(GridEight, self).__init__(N=1, include_self=include_self)


grid_eight = GridEight()
