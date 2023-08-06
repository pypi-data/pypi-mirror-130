# -*- coding: utf-8 -*-

import jax.numpy as jnp
import numpy as np
from scipy.spatial.distance import squareform, pdist

import brainpy.math as bm
from brainpy import tools
from .function import f_without_jaxarray_return

__all__ = [
  'get_sign',
  'get_sign2',
  'keep_unique',
  'rescale',
  'unknown_symbol',
]


def get_sign(f, xs, ys):
  f = f_without_jaxarray_return(f)
  xs = xs.value if isinstance(xs, bm.JaxArray) else xs
  ys = ys.value if isinstance(ys, bm.JaxArray) else ys
  Y, X = jnp.meshgrid(ys, xs)
  return jnp.sign(f(X, Y))


def get_sign2(f, *xyz, args=()):
  in_axes = tuple(range(len(xyz))) + tuple([None] * len(args))
  f = bm.jit(bm.vmap(f_without_jaxarray_return(f), in_axes=in_axes))
  xyz = tuple((v.value if isinstance(v, bm.JaxArray) else v) for v in xyz)
  XYZ = jnp.meshgrid(*xyz)
  XYZ = tuple(jnp.moveaxis(v, 1, 0).flatten() for v in XYZ)
  shape = (len(v) for v in xyz)
  return jnp.sign(f(*(XYZ + args))).reshape(shape)


def keep_unique(candidates, tol=2.5e-2, verbose=False):
  """Filter unique fixed points by choosing a representative within tolerance.

  Parameters
  ----------
  candidates: np.ndarray
    The fixed points with the shape of (num_point, num_dim).

  Returns
  -------
  fps_and_ids : tuple
    A 2-tuple of (kept fixed points, ids of kept fixed points).
  """
  keep_ids = np.arange(candidates.shape[0])
  if tol <= 0.0:
    return candidates, keep_ids
  if candidates.shape[0] <= 1:
    return candidates, keep_ids

  nfps = candidates.shape[0]
  all_drop_idxs = []

  # If point a and point b are within identical_tol of each other, and the
  # a is first in the list, we keep a.
  example_idxs = np.arange(nfps)
  distances = squareform(pdist(candidates, metric="euclidean"))
  for fidx in range(nfps - 1):
    distances_f = distances[fidx, fidx + 1:]
    drop_idxs = example_idxs[fidx + 1:][distances_f <= tol]
    all_drop_idxs += list(drop_idxs)

  unique_dropidxs = np.unique(all_drop_idxs)
  keep_ids = np.setdiff1d(example_idxs, unique_dropidxs)
  if keep_ids.shape[0] > 0:
    unique_fps = candidates[keep_ids, :]
  else:
    unique_fps = np.array([], dtype=np.int64)

  if verbose:
    print(f"    Kept {unique_fps.shape[0]}/{nfps} unique fixed points "
          f"with uniqueness tolerance {tol}.")

  return unique_fps, keep_ids



def rescale(min_max, scale=0.01):
  """Rescale lim."""
  min_, max_ = min_max
  length = max_ - min_
  min_ -= scale * length
  max_ += scale * length
  return min_, max_


def unknown_symbol(expr, scope):
  """Examine where the given expression ``expr`` has the unknown symbol in ``scope``.
  """
  ids = tools.get_identifiers(expr)
  ids = set([id_.split('.')[0].strip() for id_ in ids])
  return ids - scope
