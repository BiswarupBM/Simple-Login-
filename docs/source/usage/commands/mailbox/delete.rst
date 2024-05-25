mailbox delete
==============

.. code-block:: console

   Usage: simplelogin mailbox delete [OPTIONS] ID
   
     Delete the mailbox with the given `ID`, optionally transferring all its
     aliases to another mailbox
   
   Options:
     -t, --transfer-aliases-to INTEGER
                                     The ID of the mailbox which is to take over
                                     the deleted mailbox's aliases. A value -1
                                     indicates that all the aliases belonging to
                                     the deleted mailbox are also to be deleted.
                                     If this is the case, a confirmation prompt
                                     will appear unless the -y flag is also set.
                                     [default: -1]
     -y, --yes                       if `--transfer-aliases-to` is -1, set this
                                     flag to bypass a confirmation prompt. It has
                                     no effect if `-t` has another value.
     -h, --help                      Show this message and exit.
   
     Note that SimpleLogin does not currently support this command.
