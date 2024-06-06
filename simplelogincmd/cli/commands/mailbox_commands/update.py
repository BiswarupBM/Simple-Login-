import click

from simplelogincmd.cli import const


@click.command(
    "update",
    short_help=const.HELP.MAILBOX.UPDATE.SHORT,
    help=const.HELP.MAILBOX.UPDATE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-e",
    "--email",
    help=const.HELP.MAILBOX.UPDATE.OPTION.EMAIL,
)
@click.option(
    "-d/-D",
    "--default/--no-default",
    default=None,
    help=const.HELP.MAILBOX.UPDATE.OPTION.DEFAULT,
)
@click.option(
    "-c/-C",
    "--cancel-email-change/--no-cancel-email-change",
    default=None,
    help=const.HELP.MAILBOX.UPDATE.OPTION.CANCEL_EMAIL_CHANGE,
)
def update(
    id: str,
    email: str | None,
    default: bool | None,
    cancel_email_change: bool | None,
) -> bool:
    """Modify a mailbox's attributes"""
    from simplelogincmd.cli.commands.mailbox_commands._update import _update

    return _update(id, email, default, cancel_email_change)
