*************************
pyprojstencil
*************************

Gist
==========

Source Code Repository
---------------------------

|source| `Repository <https://github.com/pradyparanjpe/pyprojstencil.git>`__


Badges
---------

|Documentation Status|  |Coverage|  |PyPi Version|  |PyPi Format|  |PyPi Pyversion|


Description
==============

Create a python project from template.

What does it do
--------------------

Create a python `project` tree with the following features
  - git init
  - virtualenv ``.venv`` located in `project's` root
  - docs (sphinx-readthedocs)
  - unit tests
  - coverage report
  - code-aid for planning ``plan.org`` and common actions
    - init_venv (initialize venv with linter, importmagic, etc)
    - install (install in local environment)
    - coverage (test code and create a coverage badge)
    - pypi (upload to testpypi repository)

.. |Documentation Status| image:: https://readthedocs.org/projects/pyprojstencil/badge/?version=latest
   :target: https://pyprojstencil.readthedocs.io/?badge=latest
.. |source| image:: https://github.githubassets.com/favicons/favicon.png
   :target: https://github.com/pradyparanjpe/pyprojstencil.git

.. |PyPi Version| image:: https://img.shields.io/pypi/v/pyprojstencil
   :target: https://pypi.org/project/pyprojstencil/
   :alt: PyPI - version

.. |PyPi Format| image:: https://img.shields.io/pypi/format/pyprojstencil
   :target: https://pypi.org/project/pyprojstencil/
   :alt: PyPI - format

.. |PyPi Pyversion| image:: https://img.shields.io/pypi/pyversions/pyprojstencil
   :target: https://pypi.org/project/pyprojstencil/
   :alt: PyPi - pyversion

.. |Coverage| image:: docs/coverage.svg
   :alt: tests coverage
   :target: tests/htmlcov/index.html
