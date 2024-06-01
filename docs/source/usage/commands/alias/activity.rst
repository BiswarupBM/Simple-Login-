alias activity
==============

.. code-block:: console

   Usage: simplelogin alias activity [OPTIONS] ID

     List activity for the alias with the given ID. `ID` can be the alias's
     numeric id or, if you have a local database, either its email address or
     note. In the latter cases, if more than one alias matches, you will be
     prompted to choose one.

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

     Show only action and from_ fields: `list -i 'action,from_'`

     Show all fields except for reverse_alias: `list -e 'reverse_alias'`

     Show action, from_, and reverse_alias fields, except for reverse_alias:
     `list -i 'action,from_,reverse_alias' -e 'reverse_alias'` (this is more
     easily expressed as `list -i 'action,from_'`, but it is possible to use both
     options together nonetheless.)

     Valid fields: action, from_, to_, timestamp, reverse_alias,
     reverse_alias_address
