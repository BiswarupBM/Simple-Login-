"""
Exceptions raised for usage errors, bad inputs, etc.
"""

from click.exceptions import ClickException

from simplelogincmd.cli import const


# Inherit from `ClickException` instead of `UsageError` to avoid
# showing command context, which isn't relevant to this sort of error.
class NotLoggedInError(ClickException):
    """
    Raised when an unauthenticated user attempts to access protected data

    This inherits from :class:`click.ClickException` rather than
    :class:`click.UsageError` to avoid showing the current context,
    which is not relevant to this sort of error, along with the error
    message.
    """

    exit_code = const.EXIT_CODE.NOT_LOGGED_IN

    def __init__(self, message: str | None = None) -> None:
        message = message or "You must log in first."
        super().__init__(message)
