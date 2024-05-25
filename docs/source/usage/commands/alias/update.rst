alias update
============

.. code-block:: console

   Usage: simplelogin alias update [OPTIONS] ID
   
     Modify the alias with the given `ID`
   
   Options:
     -n, --note TEXT                 Attach a note to the item. Setting this
                                     switch without providing any value will open
                                     an editor in which you can enter the note.
     -a, --name TEXT                 The name that will appear as the user of the
                                     alias
     -m, --mailbox TEXT              The ID(s) or email address(es) of the
                                     mailbox(es) to which the alias belongs. use
                                     this multiple times to enter multiple
                                     mailboxes. At least one is required.
                                     [required]
     -d, --disable-pgp / -D, --no-disable-pgp
                                     Whether to disable PGP
     -p, --pinned / -P, --no-pinned  Whether to pin the alias
     -h, --help                      Show this message and exit.
