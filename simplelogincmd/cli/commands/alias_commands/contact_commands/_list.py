import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


def _list(id, include, exclude):
    fields = util.get_display_fields_from_options(
        const.CONTACT_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
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
