from simplelogincmd.database.models import (
    Alias,
    Mailbox,
    Object,
)


def test_init_accepts_extra_arguments():
    # No asserts necessary. Only testing that __init__ does not raise.
    Alias(extratestkwarg=True)
    Mailbox(extratestkwarg=True)
