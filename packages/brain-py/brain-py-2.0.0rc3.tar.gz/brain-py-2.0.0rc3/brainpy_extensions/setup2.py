# -*- coding: utf-8 -*-

import os
import re

from pybind11.setup_helpers import Pybind11Extension
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext


# version control
HERE = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(HERE, 'brainpylib', '__init__.py'), 'r') as f:
  init_py = f.read()
  __version__ = re.search('__version__ = "(.*)"', init_py).groups()[0]
cuda_version = os.environ.get("JAX_CUDA_VERSION")
if cuda_version:
  __version__ += "+cuda" + cuda_version.replace(".", "")

# extension modules
ext_modules = [
  Pybind11Extension("brainpylib/cpu_ops",
                    ["lib/cpu_ops.cc", ],
                    define_macros=[('VERSION_INFO', '0.02')]),
]

# build
setup(
  name='brainpylib',
  version=__version__,
  description='C++/CUDA Library for BrainPy',
  author='BrainPy team',
  author_email='chao.brain@qq.com',
  packages=find_packages(exclude=['lib*']),
  include_package_data=True,
  install_requires=["jax", "jaxlib"],
  extras_require={"test": "pytest"},
  python_requires='>=3.6',
  url='https://github.com/PKU-NIP-Lab/BrainPy',
  ext_modules=ext_modules,
  cmdclass={"build_ext": build_ext},
)
