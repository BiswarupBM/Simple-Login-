import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


@click.command(
    "create",
    short_help=const.HELP.ALIAS.CONTACT.CREATE.SHORT,
    help=const.HELP.ALIAS.CONTACT.CREATE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-e",
    "--email",
    help=const.HELP.ALIAS.CONTACT.CREATE.OPTION.EMAIL,
)
@click.pass_obj
@util.authenticate
def contact_create(obj, id: int, email: str) -> bool:
    """Create a new contact"""
    sl, db = obj.sl, obj.db
    id = util.resolve_id(db, Alias, id)
    success, obj = sl.create_contact(id, email)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.reverse_alias_address)
    return True
