###################
USER-CONFIGURATION
###################

Configuration file is in `yaml <https://yaml.org/spec/>`__
format.

********************************
Location of configuration files
********************************

Configuration may be specified at the following locations:

User (XDG_CONFIG_HOME):
========================

This variable is generally set to ``$HOME/.config`` on unix-like
systems. Even if unset, we will still try the ``$HOME/.config``
directory.

``$XFG_CONFIG_HOME/ppstencil.yml``

OR, may be submitted using the command line flag `-c`

*********************
Configuration format
*********************
Following keys are accepted with string values;
all other keys are rejected.

- **version**: program version
- **description**: program description
- **years**: copyright years
- **license**: (case-sensitive) [currently available: LGPLv3, GPLv3, Apache, MIT]
- **license_header**: custom license header
- **pyversion**: python version for virtual environment
- **author**: Full name of author
- **email**: Email address of author
- **url**: Project URL
- **uname**: username of author (git, pypi, etc)
- **githost**: e.g. github, gitlab, etc.
- **branch**: default starting branch

Example:
==========

.. code:: yaml
  :name: ${HOME}/.config/ppstencil.yml

    version: "0!0.0dev0"
    description: "A Useful project"
    years: "2020-2021"
    license: "LGPLv3"
    pyversion: "3"
    author: "Pradyumna Paranjape"
    email: "pradyparanjpe@rediffmail.com"
    url: "https://github.com/pradyparanjpe/pyprojstencil.git"
    uname: "pradyparanjpe"
    githost: "github"
    branch: "master"

.. warning::

  - all values in the configuration file will be converted to ``str``.
