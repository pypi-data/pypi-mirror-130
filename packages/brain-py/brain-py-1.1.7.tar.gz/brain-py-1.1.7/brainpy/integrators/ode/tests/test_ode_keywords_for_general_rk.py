# -*- coding: utf-8 -*-

import pytest

import numpy as np
from brainpy import errors
from brainpy.integrators.ode import odeint


def test_euler():
  print('Test Euler method:')
  print()
  odeint(method='euler', show_code=True, f=lambda v, t, p: t)

  with pytest.raises(errors.CodeError):
    odeint(method='euler', show_code=True, f=lambda f, t, dt: t)

  with pytest.raises(errors.CodeError):
    odeint(method='euler', show_code=True, f=lambda v, t, dt: t)

  with pytest.raises(errors.CodeError):
    odeint(method='euler', show_code=True, f=lambda v, t, v_new: t)

  with pytest.raises(errors.CodeError):
    odeint(method='euler', show_code=True, f=lambda v, t, dv_k1: t)

  print('-' * 40)

# def test_euler2():
#   print('Test Euler method:')
#   print()
#
#   def func(self, m, t, V):
#     alpha = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
#     beta = self.a * np.exp(-(V + 65) / 18)
#     dmdt = alpha * (1 - m) - beta * m
#     return dmdt
#   odeint(method='euler', show_code=True, f=func)


def test_order2_rk():
  for method in ['heun2', 'midpoint', 'ralston2']:
    print(f'Test {method} method:')
    print()
    odeint(method=method, show_code=True, f=lambda v, t, p: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda f, t, dt: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dt: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, v_new: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k1: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k2: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k2_v_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k2_t_arg: t)

    print('-' * 40)


def test_rk2():
  method = 'rk2'

  print(f'Test {method} method:')
  print()
  odeint(method=method, show_code=True, f=lambda v, t, p: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda f, t, dt: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda v, t, dt: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda v, t, v_new: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda v, t, dv_k1: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda v, t, dv_k2: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda v, t, k2_v_arg: t)

  with pytest.raises(errors.CodeError):
    odeint(method=method, show_code=True, f=lambda v, t, k2_t_arg: t)

  print('-' * 40)


def test_order3_rk():
  for method in ['rk3', 'heun3', 'ralston3', 'ssprk3']:
    print(f'Test {method} method:')
    print()
    odeint(method=method, show_code=True, f=lambda v, t, p: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda f, t, dt: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dt: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, v_new: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k1: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k2: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k3: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k2_v_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k2_t_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k3_v_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k3_t_arg: t)

    print('-' * 40)


def test_order4_rk():
  for method in ['rk4', 'ralston4', 'rk4_38rule']:
    print(f'Test {method} method:')
    print()
    odeint(method=method, show_code=True, f=lambda v, t, p: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda f, t, dt: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dt: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, v_new: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k1: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k2: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k3: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, dv_k4: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k2_v_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k2_t_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k3_v_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k3_t_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k4_v_arg: t)

    with pytest.raises(errors.CodeError):
      odeint(method=method, show_code=True, f=lambda v, t, k4_t_arg: t)

    print('-' * 40)

# if __name__ == '__main__':
#     test_euler()
#     test_order2_rk()
#     test_rk2()
#     test_order3_rk()
#     test_order4_rk()
