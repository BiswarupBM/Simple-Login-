alias custom
============

.. code-block:: console

   Usage: simplelogin alias custom [OPTIONS]
   
     Create a new custom alias
   
   Options:
     -o, --hostname TEXT          The website with which the new alias is
                                  associated
     -p, --prefix TEXT            The new alias's prefix, the part that appears
                                  before the `.`. If not given, you will be
                                  prompted for a value, if `-h` is set and `-y`
                                  is not, or if `-h` is not specified. This is
                                  because a prefix is required, but SimpleLogin
                                  can suggest one itself based on a hostname.
     -m, --mailbox TEXT           The ID(s) or email address(es) of the
                                  mailbox(es) to which the new alias will belong.
                                  use this multiple times to enter multiple
                                  mailboxes. At least one is required.
                                  [required]
     -n, --note TEXT              Attach a note to the item. Setting this switch
                                  without providing any value will open an editor
                                  in which you can enter the note.
     -a, --name TEXT              The name that will appear as the user of the
                                  new alias
     -s, --select-suffix INTEGER  Automatically select the nth suffix, bypassing
                                  the prompt as long as n is >= 0 and < the
                                  number of suffixes offered. A value of 0 refers
                                  to the first suffix.
     -y, --yes                    Bypass confirmation prompts where possible
     -h, --help                   Show this message and exit.
