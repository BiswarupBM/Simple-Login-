alias contact list
==================

.. code-block:: console

   Usage: simplelogin alias contact list [OPTIONS] ID
   
     List contacts for the alias with the given `ID`
   
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
   
     Show only id and contact fields: `list -i 'id,contact'`
   
     Show all fields except for block_forward: `list -e 'block_forward'`
   
     Show id, contact, and block_forward fields, except for block_forward: `list
     -i 'id,contact,block_forward' -e 'block_forward'` (this is more easily
     expressed as `list -i 'id,contact'`, but it is possible to use both options
     together nonetheless.)
   
     Valid fields: id, contact, reverse_alias, reverse_alias_address,
     block_forward, last_email_sent_timestamp, creation_timestamp
