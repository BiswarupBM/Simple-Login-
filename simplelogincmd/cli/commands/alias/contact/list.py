import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


@click.command(
    "list",
    short_help=const.HELP.ALIAS.CONTACT.LIST.SHORT,
    help=const.HELP.ALIAS.CONTACT.LIST.LONG,
    epilog=const.HELP.ALIAS.CONTACT.LIST.EPILOG,
)
@click.argument(
    "id",
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.CONTACT.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.CONTACT.LIST.OPTION.EXCLUDE,
)
@click.pass_obj
@util.authenticate
def contact_list(obj, id: int, include: str | None, exclude: str | None) -> None:
    """List contacts in a tabular format"""
    sl, db, cfg = obj.sl, obj.db, obj.cfg
    fields = util.get_display_fields_from_options(
        const.CONTACT_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    id = util.resolve_id(db, Alias, id)
    contacts = sl.get_all_alias_contacts(id)
    if len(contacts) == 0:
        click.echo("No contacts found")
        return
    for contact in contacts:
        db.session.upsert(contact)
    db.session.commit()
    pager_threshold = cfg.get("display.pager-threshold")
    util.display_model_list(contacts, fields, pager_threshold)
