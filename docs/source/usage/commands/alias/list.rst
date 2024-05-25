alias list
==========

.. code-block:: console

   Usage: simplelogin alias list [OPTIONS]
   
     List all your aliases
   
   Options:
     -i, --include TEXT  A comma-separated list of fields to include in the
                         resulting table. Only fields in this list will appear.
                         Omit this option to show all fields.
     -e, --exclude TEXT  A comma-separated list of fields to exclude from the
                         resulting table. Useful if you want to view most fields
                         but leave a few out, rather than specifying a longer
                         list with `--include`.
     -p, --pinned        Get only pinned aliases
     -n, --enabled       Get only enabled aliases
     -d, --disabled      Get only disabled aliases
     -h, --help          Show this message and exit.
   
     Examples
   
     Show only id and email fields: `list -i 'id,email'`
   
     Show all fields except for name: `list -e 'name'`
   
     Show id, email, and name fields, except for name: `list -i 'id,email,name'
     -e 'name'` (this is more easily expressed as `list -i 'id,email'`, but it is
     possible to use both options together nonetheless.)
   
     Valid fields: id, email, name, note, enabled, nb_block, nb_forward,
     nb_reply, mailboxes, latest_activity, support_pgp, disable_pgp, pinned,
     creation_timestamp
