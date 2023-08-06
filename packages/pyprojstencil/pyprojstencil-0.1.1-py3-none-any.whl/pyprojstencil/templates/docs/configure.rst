####################
USER-CONFIGURATION
####################

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

``$XFG_CONFIG_HOME/<PROJECT>/config.yml``

*********************
Configuration format
*********************

Following objects are accepted:

  - keys: value

Example:
==========

.. code:: yaml
  :name: ${HOME}/.config/<PROJECT>.yml

    key: value
