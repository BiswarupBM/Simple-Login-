SimpleLogin-CLI Usage
=====================

Installation
------------

via pipx
^^^^^^^^

The recommended method of installation is via `pipx`_. This allows the
application to be installed in an environment isolated from other
packages and apps, while being made available in your usual shell at
all times.

.. code-block:: console

   pipx install simplelogincmd

via pip
^^^^^^^

.. code-block:: console

   pip install simplelogincmd

Getting Started
---------------

You invoke the program via the ``simplelogin`` command. All commands offer help via the ``-h`` or ``--help`` options, as well as provide context-sensitive help when they are misused.

Shortening the ``simplelogin`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A note for those perhaps newer to CLI usage. It is possible to alias
commands to make them easier to type. For example, to permit the use
of ``sl`` rather than ``simplelogin`` in Bash, you could add the
following to your ``.bashrc``:

.. code-block:: console

   alias sl=simplelogin

SimpleLogin-CLI does not do this for you to avoid clashes with already-
existing commands. Consult your own shell's documentation for aliasing
instructions.

Command help pages
^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   commands/overview

.. _pipx: https://pipx.pypa.io/
