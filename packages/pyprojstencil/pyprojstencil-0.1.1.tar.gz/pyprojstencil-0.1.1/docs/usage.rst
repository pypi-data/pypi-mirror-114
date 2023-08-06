#######
USAGE
#######


**********
SYNOPSIS
**********

.. argparse::
   :ref: pyprojstencil.command_line._cli
   :prog: pyprojstencil

**************
Instructions
**************

User configuration
====================

- Create a configuration file as directed `here <configure.html>`__.

Initialize python project
===========================

Run this script
-----------------

- For each new python project e.g. ``myproject``, initiate the project in its intended parent folder e.g. ``${HOME}/Languages/python``:

.. code:: sh

   cd "${PY_CODES:-${HOME}/Languages/python}"
   pyprojstencil myproject


Use virtual environment
-------------------------

- Activate project's `virtual environment <https://pypi.org/project/virtualenv/>`__

.. code:: sh

   source myproject/.venv/bin/activate

.. warning::

   All further instructions are provided with the assumption that project's own virtual environment is active. If no virtual environment is active, a *warning* may be displayed before running environment-sensitive action. If **some** virtual environment is active, programs will get installed in **that** environment, leading to a lot of confusion.

Install coding aids
---------------------

- Initialize python coding aids:

.. code:: sh

   cd myproject
   code-aid/init_venv.sh

.. note::
   - aid modules are listed in ``code-aid/requirements.txt``
   - the directory `code-aids` is meant to aid while coding. It is listed in ``.gitignore`` and is never tracked or published.


Code
======

Algorithm
-----------

- Plan the project by editing the file ``code-aid/plan.org`` see: `Org-mode <https://orgmode.org>`__

Code
------

- Write source-code for `myproject` in the subfolder which is also named ``myproject``

Version control
-----------------

- The default git branch is `pagan`
- A `develop` branch may be created by trimming history from `pagan` after the project draft is ready.

  - Frequently saving, staging-committing files in the VCS is a good habit.

.. code::

   git add -A
   git commit -m "commit message on $(date)"

Build
=======

requirements
--------------

- revisit requirements using `pigar <https://pypi.org/project/pigar/>`__

.. code:: sh

   pigar

Install script setup
----------------------

- Suitably edit ``setup.cfg``

- Install the project in its virtual environment

.. code:: sh

   code-aid/install.sh


Test coverage
===============

- Write unit tests in folder ``tests``
- Run unit tests and generate coverage reports

.. code:: sh

   code-aid/coverage.sh

.. note::

   - tests are run with `pytest <https://pypi.org/project/pytest/>`__
   - html coverage report is generated in ``tests/htmlcov`` using `coverage <https://pypi.org/project/coverage/>`__
   - coverage-badge is generated using `coverage-badge <https://pypi.org/project/coverage-badge/>`__


Documentation
===============

- Edit and complete the `sphinx <https://pypi.org/project/Sphinx/>`__ documentation from a raw draft in folder ``docs`` and run

.. code:: sh

   cd docs
   make html
   cd ..

.. note::
   - various modules used for sphinx documentation are listed in ``docs/requirements.txt``


- edit ``.readthedocs.yml`` file suitably before adding project documentation hook

Publish
=========

MANIFEST.in
-------------

- Confirm that all files are included in project builds

.. code:: sh

   check-manifest

pip
-----
- Publish project

.. code:: sh

   code-aid/pypi.sh
