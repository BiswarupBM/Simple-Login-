config
======

.. code-block:: console

   Usage: simplelogin config [OPTIONS] KEY [VALUE] COMMAND [ARGS]...

     Display (or set to VALUE) the config option KEY

   Options:
     -l, --list          List all configuration options and exit
     --restore-defaults  Restore all settings to their default values and exit
     -h, --help          Show this message and exit.

     Boolean options accept `true/false`, `on/off`, or `yes/no` as values

options
-------

Below is the current list of valid configuration options, along with 
their default values and an explanation of their meaning.

api.api-key = ********************
   Your SimpleLogin API key. The :doc:`login <../account/login>` command
   sets this value, but you may set it manually here if, for instance,
   you already have a valid key you want to use.
display.pager-threshold = 20
   Commands that output several lines will do so via a pager if the
   output consists of this many lines or more. Setting it to 0 will
   indicate that the pager is never to be used.
