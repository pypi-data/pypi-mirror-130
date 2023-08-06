# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pytest

import brainpy as bp


def test_random_prob():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    conn1 = bp.connect.FixedProb(prob=0.1, seed=123)
    conn1(pre_size=(10, 20), post_size=(10, 20))
    pre_ids, post_ids = conn1.require('pre_ids', 'post_ids')

    conn2 = bp.connect.FixedProb(prob=0.1, seed=123)
    conn2(pre_size=(10, 20), post_size=(10, 20))
    mat = conn2.require(bp.connect.CONN_MAT)
    pre_ids2, post_ids2 = bp.math.where(mat)


def test_random_fix_pre1():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    for num in [0.4, 20]:
      conn1 = bp.connect.FixedPreNum(num, seed=1234)(pre_size=(10, 15), post_size=(10, 20))
      mat1 = conn1.require(bp.connect.CONN_MAT)

      conn2 = bp.connect.FixedPreNum(num, seed=1234)(pre_size=(10, 15), post_size=(10, 20))
      mat2 = conn2.require(bp.connect.CONN_MAT)

      assert bp.math.array_equal(mat1, mat2)


def test_random_fix_pre2():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    for num in [0.5, 3]:
      conn1 = bp.connect.FixedPreNum(num, seed=1234)(pre_size=5, post_size=4)
      mat1 = conn1.require(bp.connect.CONN_MAT)
      print(mat1)


def test_random_fix_pre3():
  bp.math.use_backend('numpy')
  conn1 = bp.connect.FixedPreNum(num=6, seed=1234)(pre_size=3, post_size=4)
  with pytest.raises(AssertionError):
    conn1.require(bp.connect.CONN_MAT)


def test_random_fix_post1():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    for num in [0.4, 20]:
      conn1 = bp.connect.FixedPostNum(num, seed=1234)(pre_size=(10, 15), post_size=(10, 20))
      mat1 = conn1.require(bp.connect.CONN_MAT)

      conn2 = bp.connect.FixedPostNum(num, seed=1234)(pre_size=(10, 15), post_size=(10, 20))
      mat2 = conn2.require(bp.connect.CONN_MAT)

      assert bp.math.array_equal(mat1, mat2)


def test_random_fix_post2():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    for num in [0.5, 3]:
      conn1 = bp.connect.FixedPostNum(num, seed=1234)(pre_size=5, post_size=4)
      mat1 = conn1.require(bp.connect.CONN_MAT)
      print(mat1)


def test_random_fix_post3():
  bp.math.use_backend('numpy')
  conn1 = bp.connect.FixedPostNum(num=6, seed=1234)(pre_size=3, post_size=4)
  with pytest.raises(AssertionError):
    conn1.require(bp.connect.CONN_MAT)


def test_gaussian_prob1():
  bp.math.use_backend('numpy')
  conn = bp.connect.GaussianProb(sigma=1.)(pre_size=100)
  mat = conn.require(bp.connect.CONN_MAT)

  # plt.imshow(mat)
  # plt.show()


def test_gaussian_prob2():
  bp.math.use_backend('numpy')

  conn = bp.connect.GaussianProb(sigma=4)(pre_size=(50, 50))
  mat = conn.require(bp.connect.CONN_MAT)

  # plt.imshow(mat)
  # plt.show()

  # plt.imshow(mat[0].reshape(conn.pre_size))
  # plt.show()


def test_gaussian_prob3():
  bp.math.use_backend('numpy')
  conn = bp.connect.GaussianProb(sigma=4, periodic_boundary=True)(pre_size=(50, 50))
  mat = conn.require(bp.connect.CONN_MAT)

  # plt.imshow(mat)
  # plt.show()

  # plt.imshow(mat[0].reshape(conn.pre_size))
  # plt.show()


def test_gaussian_prob4():
  bp.math.use_backend('numpy')
  conn = bp.connect.GaussianProb(sigma=4, periodic_boundary=True)(pre_size=(20, 20, 20))
  conn.require(bp.connect.CONN_MAT,
               bp.connect.PRE_IDS, bp.connect.POST_IDS,
               bp.connect.PRE2POST, bp.connect.POST_IDS)


def test_SmallWorld1():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    conn = bp.connect.SmallWorld(num_neighbor=2, prob=0.5)
    conn(pre_size=(20, 3), post_size=(20, 3))
    with pytest.raises(NotImplementedError):
      conn.require(bp.connect.CONN_MAT)


def test_SmallWorld2():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    conn = bp.connect.SmallWorld(num_neighbor=2, prob=0.5)
    conn(pre_size=(100,), post_size=(100,))
    conn.require(bp.connect.CONN_MAT,
                 bp.connect.PRE_IDS, bp.connect.POST_IDS,
                 bp.connect.PRE2POST, bp.connect.POST_IDS)


def test_ScaleFreeBA():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    conn = bp.connect.ScaleFreeBA(m=2)
    for size in [100, (10, 20), (2, 10, 20)]:
      conn(pre_size=size, post_size=size)
      conn.require(bp.connect.CONN_MAT,
                   bp.connect.PRE_IDS, bp.connect.POST_IDS,
                   bp.connect.PRE2POST, bp.connect.POST_IDS)


def test_ScaleFreeBADual():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    conn = bp.connect.ScaleFreeBADual(m1=2, m2=3, p=0.4)
    for size in [100, (10, 20), (2, 10, 20)]:
      conn(pre_size=size, post_size=size)
      conn.require(bp.connect.CONN_MAT,
                   bp.connect.PRE_IDS, bp.connect.POST_IDS,
                   bp.connect.PRE2POST, bp.connect.POST_IDS)


def test_PowerLaw():
  for bk in ['numpy', 'jax']:
    bp.math.use_backend(bk)

    conn = bp.connect.PowerLaw(m=3, p=0.4)
    for size in [100, (10, 20), (2, 10, 20)]:
      conn(pre_size=size, post_size=size)
      conn.require(bp.connect.CONN_MAT,
                   bp.connect.PRE_IDS, bp.connect.POST_IDS,
                   bp.connect.PRE2POST, bp.connect.POST_IDS)
