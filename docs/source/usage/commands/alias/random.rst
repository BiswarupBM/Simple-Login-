alias random
============

.. code-block:: console

   Usage: simplelogin alias random [OPTIONS]
   
     Create a new random alias
   
   Options:
     -o, --hostname TEXT  The website with which the new alias is associated
     -u, --uuid           UUID mode: generate an alias based on a random series
                          of numbers and letters
     -w, --word           Word mode: Generate an alias based on a random series
                          of words
     -n, --note TEXT      Attach a note to the item. Setting this switch without
                          providing any value will open an editor in which you
                          can enter the note.
     -h, --help           Show this message and exit.
   
     The `--uuid` and `--word` options are exclusive - only one, not both, may be
     specified. If both appear, the last one wins.
