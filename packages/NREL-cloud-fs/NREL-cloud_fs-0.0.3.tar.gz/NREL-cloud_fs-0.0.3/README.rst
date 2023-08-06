*******************************************
Welcome to the cloud file system utilities!
*******************************************

.. image:: https://github.com/NREL/cloud_fs/workflows/Documentation/badge.svg
    :target: https://nrel.github.io/cloud_fs/

.. image:: https://github.com/NREL/cloud_fs/workflows/Pytests/badge.svg
    :target: https://github.com/NREL/cloud_fs/actions?query=workflow%3A%22Pytests%22

.. image:: https://github.com/NREL/cloud_fs/workflows/Lint%20Code%20Base/badge.svg
    :target: https://github.com/NREL/cloud_fs/actions?query=workflow%3A%22Lint+Code+Base%22

.. image:: https://img.shields.io/pypi/pyversions/NREL-cloud_fs.svg
    :target: https://pypi.org/project/NREL-cloud_fs/

.. image:: https://badge.fury.io/py/NREL-cloud_fs.svg
    :target: https://badge.fury.io/py/NREL-cloud_fs

.. image:: https://anaconda.org/nrel/nrel-cloud_fs/badges/version.svg
    :target: https://anaconda.org/nrel/nrel-cloud_fs

.. image:: https://anaconda.org/nrel/nrel-cloud_fs/badges/license.svg
    :target: https://anaconda.org/nrel/nrel-cloud_fs

.. image:: https://codecov.io/gh/nrel/cloud_fs/branch/master/graph/badge.svg?token=3J5M44VAA9
    :target: https://codecov.io/gh/nrel/cloud_fs

`cloud-fs` is a generalized file-system handler that will dynamically determine
if files are local or on the cloud (currently AWS) and perform basic
file-systm operations.

.. inclusion-intro

Installing cloud_fs
===================

Option 1: Install from PIP or Conda (recommended for analysts):
---------------------------------------------------------------

1. Create a new environment:
    ``conda create --name cloud_fs python=3.7``

2. Activate directory:
    ``conda activate cloud_fs``

3. Install cloud_fs:
    1) ``pip install NREL-cloud_fs`` or
    2) ``conda install nrel-cloud_fs --channel=nrel``


Option 2: Clone repo (recommended for developers)
-------------------------------------------------

1. from home dir, ``git clone https://github.com/NREL/cloud_fs.git``
    1) enter github username
    2) enter github password

2. Create ``cloud_fs`` environment and install package
    1) Create a conda env: ``conda create -n cloud_fs``
    2) Run the command: ``conda activate cloud_fs``
    3) cd into the repo cloned in 1.
    4) prior to running ``pip`` below, make sure the branch is correct (install
       from master!)
    5) Install ``cloud_fs`` and its dependencies by running:
       ``pip install .`` (or ``pip install -e .`` if running a dev branch
       or working on the source code)
