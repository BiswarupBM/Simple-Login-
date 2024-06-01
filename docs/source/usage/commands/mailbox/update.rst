mailbox update
==============

.. code-block:: console

   Usage: simplelogin mailbox update [OPTIONS] ID

     Modify the mailbox with the given ID. `ID` can be the mailbox's numeric id
     or, if you have a local database, its email address. In the latter case, if
     more than one mailbox matches, you will be prompted to choose one.

   Options:
     -e, --email TEXT                A new email address to assign to this
                                     mailbox
     -d, --default / -D, --no-default
                                     Whether to make this the default mailbox
     -c, --cancel-email-change / -C, --no-cancel-email-change
     -h, --help                      Show this message and exit.
