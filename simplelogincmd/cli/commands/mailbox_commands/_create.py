import click

from simplelogincmd.cli import util


def _create(email):
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    success, msg = sl.create_mailbox(email)
    if not success:
        click.echo(msg)
        return False
    click.echo(f"A verification email has been sent to {email}.")
    return True
