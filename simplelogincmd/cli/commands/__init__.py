"""
CLI application commands

There is usually no need to import and add commands or groups to the
main Click group manually. The setup script handles that automatically,
assuming the following.

* Every object that needs to be added to the main group is itself a
  group, not a command. This is because the application is designed
  to offer arbitrarily-nested commands.
* Every group which should be added is public, and any groups nested
  under those are private (i.e., their names begin with an
  underscore). This allows groups to contain other groups without polluting
  the top-level group with all the sub-subgroups.

In other words:
To create a new command, define it as a public Click group in a module 
in this package. It will be imported and added automatically. If it
should have subgroups itself, define them as private in the same
module and add them to one of the module's public groups.

See :mod:`~simplelogincmd.cli.commands.alias` for an example of subgroups with
nested sub-subgroups.
"""
