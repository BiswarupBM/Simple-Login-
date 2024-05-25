mailbox list
============

.. code-block:: console

   Usage: simplelogin mailbox list [OPTIONS]
   
     Display all your mailboxes
   
   Options:
     -i, --include TEXT  A comma-separated list of fields to include in the
                         resulting table. Only fields in this list will appear.
                         Omit this option to show all fields.
     -e, --exclude TEXT  A comma-separated list of fields to exclude from the
                         resulting table. Useful if you want to view most fields
                         but leave a few out, rather than specifying a longer
                         list with `--include`.
     -h, --help          Show this message and exit.
   
     Examples
   
     Show only id and email fields: `list -i 'id,email'`
   
     Show all fields except for default: `list -e 'default'`
   
     Show id, email, and default fields, except for default: `list -i
     'id,email,default' -e 'default'` (this is more easily expressed as `list -i
     'id,email'`, but it is possible to use both options together nonetheless.)
   
     Valid fields: id, email, nb_alias, verified, default, creation_timestamp
