import click

from simplelogincmd.cli import const, util


@click.command(
    "create",
    short_help=const.HELP.MAILBOX.CREATE.SHORT,
    help=const.HELP.MAILBOX.CREATE.LONG,
    epilog=const.HELP.MAILBOX.CREATE.EPILOG,
)
@click.option(
    "-e",
    "--email",
    prompt=True,
    help=const.HELP.MAILBOX.CREATE.OPTION.EMAIL,
)
@click.pass_obj
@util.authenticate
def create(obj, email: str) -> bool:
    """Create a new mailbox"""
    sl = obj.sl
    success, msg = sl.create_mailbox(email)
    if not success:
        click.echo(msg)
        return False
    click.echo(f"A verification email has been sent to {email}.")
    return True
