"""
CLI constants
"""

from types import SimpleNamespace as NS


EXIT_CODE = NS(
    # Start with high value to avoid clash with possible future Click codes.
    NOT_LOGGED_IN=100,
)


# Overriding default context settings.
CONTEXT_SETTINGS = dict(
    # Allow help via `-h` as well as `--help`.
    help_option_names=["-h", "--help"],
)


# Orders in which each model's fields are displayed by default, from
# left to right.
ACTIVITY_FIELD_ORDER = (
    "action",
    "from_",
    "to_",
    "timestamp",
    "reverse_alias",
    "reverse_alias_address",
)
ALIAS_FIELD_ORDER = (
    "id",
    "email",
    "name",
    "note",
    "enabled",
    "nb_block",
    "nb_forward",
    "nb_reply",
    "mailboxes",
    "latest_activity",
    "support_pgp",
    "disable_pgp",
    "pinned",
    "creation_timestamp",
)
CONTACT_FIELD_ORDER = (
    "id",
    "contact",
    "reverse_alias",
    "reverse_alias_address",
    "block_forward",
    "last_email_sent_timestamp",
    "creation_timestamp",
)
MAILBOX_FIELD_ORDER = (
    "id",
    "email",
    "nb_alias",
    "verified",
    "default",
    "creation_timestamp",
)


# Help texts common to multiple commands/options
_HELP_ALIAS_ID = (
    "`ID` can be the alias's numeric id or, if you have a local data"
    "base, either its email address or note. In the latter cases, if "
    "more than one alias matches, you will be prompted to choose one."
)
_HELP_MAILBOX_ID = (
    "`ID` can be the mailbox's numeric id or, if you have a local data"
    "base, its email address. In the latter case, if more than one "
    "mailbox matches, you will be prompted to choose one."
)
_HELP_OPTION_NOTE = (
    "Attach a note to the item. Setting this switch with"
    "out providing any value will open an editor in which you can enter "
    "the note."
)
_HELP_LIST_INCLUDE = (
    "A comma-separated list of fields to include in the "
    "resulting table. Only fields in this list will appear. Omit this "
    "option to show all fields."
)
_HELP_LIST_EXCLUDE = (
    "A comma-separated list of fields to exclude from the "
    "resulting table. Useful if you want to view most fields but leave a "
    "few out, rather than specifying a longer list with `--include`."
)
_HELP_LIST_EPILOG = (
    "Examples\n\n"
    "Show only {field1} and {field2} fields:\n"
    "`list -i '{field1},{field2}'`\n\n"
    "Show all fields except for {field3}:\n"
    "`list -e '{field3}'`\n\n"
    "Show {field1}, {field2}, and {field3} fields, except for {field3}:\n"
    "`list -i '{field1},{field2},{field3}' -e '{field3}'`\n"
    "(this is more easily expressed as `list -i '{field1},{field2}'`, "
    "but it is possible to use both options together nonetheless.)\n\n"
    "Valid fields:\n{valid_fields}"
)


# Strings used for command help. These are organized similar to the
# organization of the commands themselves, with each main group containing
# subgroups, commands, and possible options, and each subgroup/command
# containing other subgroups, subcommands, or possible options. Groups
# and commands may contain `SHORT` help text, `LONG` help text, and
# `EPILOG` text, corresponding to Click's `short_help`, `help`, and
# `epilog` group/command arguments, respectively. Options have only one
# help text, usually named after the option itself.
HELP = NS(
    ACCOUNT=NS(
        SHORT=None,
        LONG="Account management and authentication",
        LOGIN=NS(
            SHORT=None,
            LONG="Log in to your account",
            OPTION=NS(
                EMAIL="The email address associated with the account",
                PASSWORD="The account's password",
            ),
        ),
        MFA=NS(
            SHORT=None,
            LONG="Multi-factor authentication",
            EPILOG="NOTE: You should never need to invoke this command "
            "manually. It is used during the login process if MFA is "
            "enabled on your account.",
            OPTION=NS(
                OTP="Your numeric one-time password",
                MFA_KEY="The MFA key associated with the login attempt",
            ),
        ),
        LOGOUT=NS(
            SHORT=None,
            LONG="Log out of your account",
        ),
    ),
    ALIAS=NS(
        SHORT=None,
        LONG="CRUD operations on your aliases",
        ACTIVITY=NS(
            SHORT="List alias activity",
            LONG=f"List activity for the alias with the given ID. {_HELP_ALIAS_ID}",
            EPILOG=_HELP_LIST_EPILOG.format(
                field1=ACTIVITY_FIELD_ORDER[0],
                field2=ACTIVITY_FIELD_ORDER[1],
                field3=ACTIVITY_FIELD_ORDER[4],
                valid_fields=", ".join(field for field in ACTIVITY_FIELD_ORDER),
            ),
            OPTION=NS(
                INCLUDE=_HELP_LIST_INCLUDE,
                EXCLUDE=_HELP_LIST_EXCLUDE,
            ),
        ),
        CONTACT=NS(
            SHORT=None,
            LONG="CRUD operations on alias contacts",
            CREATE=NS(
                SHORT="Create a new contact",
                LONG=f"Add a contact to the alias with the given ID`. {_HELP_ALIAS_ID}",
                OPTION=NS(
                    EMAIL="The contact's email address",
                ),
            ),
            LIST=NS(
                SHORT="List alias contacts",
                LONG="List contacts for the alias with the given `ID`",
                EPILOG=_HELP_LIST_EPILOG.format(
                    field1=CONTACT_FIELD_ORDER[0],
                    field2=CONTACT_FIELD_ORDER[1],
                    field3=CONTACT_FIELD_ORDER[4],
                    valid_fields=", ".join(field for field in CONTACT_FIELD_ORDER),
                ),
                OPTION=NS(
                    INCLUDE=_HELP_LIST_INCLUDE,
                    EXCLUDE=_HELP_LIST_EXCLUDE,
                ),
            ),
        ),
        CUSTOM=NS(
            SHORT=None,
            LONG="Create a new custom alias",
            OPTION=NS(
                HOSTNAME="The website with which the new alias is " "associated",
                PREFIX="The new alias's prefix, the part that appears "
                "before the `.`. If not given, you will be prompted "
                "for a value, if `-h` is set and `-y` is not, or "
                "if `-h` is not specified. This is because a prefix "
                "is required, but SimpleLogin can suggest one itself "
                "based on a hostname.",
                MAILBOXES="The ID(s) or email address(es) of the mail"
                "box(es) to which the new alias will belong. use this "
                "multiple times to enter multiple mailboxes. At least "
                "one is required.",
                NOTE=_HELP_OPTION_NOTE,
                NAME="The name that will appear as the user of the new " "alias",
                SELECT_SUFFIX="Automatically select the nth suffix, by"
                "passing the prompt as long as n is >= 0 and < the "
                "number of suffixes offered. A value of 0 refers to "
                "the first suffix.",
                YES="Bypass confirmation prompts where possible",
            ),
        ),
        DELETE=NS(
            SHORT="Delete an alias",
            LONG=f"Delete the alias with the given ID. {_HELP_ALIAS_ID}",
            OPTION=NS(
                YES="Bypass the confirmation prompt",
            ),
        ),
        GET=NS(
            SHORT="View a specific alias",
            LONG=f"View the alias with the given ID. {_HELP_ALIAS_ID}",
            EPILOG=_HELP_LIST_EPILOG.format(
                field1=ALIAS_FIELD_ORDER[0],
                field2=ALIAS_FIELD_ORDER[1],
                field3=ALIAS_FIELD_ORDER[2],
                valid_fields=", ".join(ALIAS_FIELD_ORDER),
            ),
            OPTION=NS(
                INCLUDE=_HELP_LIST_INCLUDE,
                EXCLUDE=_HELP_LIST_EXCLUDE,
            ),
        ),
        LIST=NS(
            SHORT=None,
            LONG="List all your aliases",
            EPILOG=_HELP_LIST_EPILOG.format(
                field1=ALIAS_FIELD_ORDER[0],
                field2=ALIAS_FIELD_ORDER[1],
                field3=ALIAS_FIELD_ORDER[2],
                valid_fields=", ".join(ALIAS_FIELD_ORDER),
            ),
            OPTION=NS(
                INCLUDE=_HELP_LIST_INCLUDE,
                EXCLUDE=_HELP_LIST_EXCLUDE,
                PINNED="Get only pinned aliases",
                ENABLED="Get only enabled aliases",
                DISABLED="Get only disabled aliases",
            ),
        ),
        RANDOM=NS(
            SHORT=None,
            LONG="Create a new random alias",
            EPILOG="The `--uuid` and `--word` options are exclusive - "
            "only one, not both, may be specified. If both appear, the "
            "last one wins.",
            OPTION=NS(
                HOSTNAME="The website with which the new alias is " "associated",
                UUID="UUID mode: generate an alias based on a random "
                "series of numbers and letters",
                WORD="Word mode: Generate an alias based on a "
                "random series of words",
                NOTE=_HELP_OPTION_NOTE,
            ),
        ),
        TOGGLE=NS(
            SHORT="Enable or disable an alias",
            LONG=f"Enable or disable the aliase with the given ID. {_HELP_ALIAS_ID}",
        ),
        UPDATE=NS(
            SHORT="Modify an existing alias",
            LONG=f"Modify the alias with the given ID. {_HELP_ALIAS_ID}",
            OPTION=NS(
                NOTE=_HELP_OPTION_NOTE,
                NAME="The name that will appear as the user of the alias",
                MAILBOXES="The ID(s) or email address(es) of the mail"
                "box(es) to which the alias belongs. use this "
                "multiple times to enter multiple mailboxes. At least "
                "one is required.",
                DISABLE_PGP="Whether to disable PGP",
                PINNED="Whether to pin the alias",
            ),
        ),
    ),
    DATABASE=NS(
        SHORT=None,
        LONG="Manage the local database",
        DELETE=NS(
            SHORT=None,
            LONG="Delete the db",
        ),
        SYNC=NS(
            SHORT="Synchronize the DB",
            LONG="Synchronize the local database with that of SimpleLogin",
            EPILOG="Note that this command will wipe any data "
            "currently stored in your local database. This should "
            "not matter to most people, so no confirmation is "
            "required.",
        ),
    ),
    MAILBOX=NS(
        SHORT=None,
        LONG="CRUD operations on your mailboxes",
        CREATE=NS(
            SHORT=None,
            LONG="Create a new mailbox",
            EPILOG="If successful, the mailbox will receive a "
            "verification email. You will need to click the link "
            "in this email in order to verify the mailbox.",
            OPTION=NS(
                EMAIL="The email address of the new mailbox",
            ),
        ),
        DELETE=NS(
            SHORT="Delete an existing mailbox",
            LONG="Delete the mailbox with the given ID, optionally "
            f"transferring all its aliases to another mailbox. {_HELP_MAILBOX_ID}",
            EPILOG="Note that SimpleLogin does not currently support " "this command.",
            OPTION=NS(
                TRANSFER_ALIASES_TO="The ID of the mailbox which is "
                "to take over the deleted mailbox's aliases. A value "
                "-1 indicates that all the aliases belonging to the "
                "deleted mailbox are also to be deleted. If this "
                "is the case, a confirmation prompt will appear unless "
                "the -y flag is also set.",
                YES="if `--transfer-aliases-to` is -1, set this flag "
                "to bypass a confirmation prompt. It has no effect "
                "if `-t` has another value.",
            ),
        ),
        LIST=NS(
            SHORT=None,
            LONG="Display all your mailboxes",
            EPILOG=_HELP_LIST_EPILOG.format(
                field1=MAILBOX_FIELD_ORDER[0],
                field2=MAILBOX_FIELD_ORDER[1],
                field3=MAILBOX_FIELD_ORDER[4],
                valid_fields=", ".join(MAILBOX_FIELD_ORDER),
            ),
            OPTION=NS(
                INCLUDE=_HELP_LIST_INCLUDE,
                EXCLUDE=_HELP_LIST_EXCLUDE,
            ),
        ),
        UPDATE=NS(
            SHORT="Update a mailbox's attributes",
            LONG=f"Modify the mailbox with the given ID. {_HELP_MAILBOX_ID}",
            OPTION=NS(
                EMAIL="A new email address to assign to this mailbox",
                DEFAULT="Whether to make this the default mailbox",
                CANCEL_EMAIL_CHANGE=None,  # What does this do?
            ),
        ),
    ),
)
