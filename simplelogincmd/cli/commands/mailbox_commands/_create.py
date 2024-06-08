import click

from simplelogincmd.cli.util import init


def _create(email):
    cfg = init.cfg()
    sl = init.sl(cfg)
    success, msg = sl.create_mailbox(email)
    if not success:
        click.echo(msg)
        return False
    click.echo(f"A verification email has been sent to {email}.")
    return True
