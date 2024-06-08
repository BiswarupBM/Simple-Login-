import click

from simplelogincmd.cli import const
from simplelogincmd.cli.util import init, output


def _list(include, exclude, query):
    fields = output.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    aliases = sl.get_all_aliases(query)
    if len(aliases) == 0:
        click.echo("No aliases found.")
        return
    for alias in aliases:
        db.session.upsert(alias)
    db.session.commit()
    pager_threshold = cfg.get("display.pager-threshold")
    output.display_model_list(aliases, fields, pager_threshold)
