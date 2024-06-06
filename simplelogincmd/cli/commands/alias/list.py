import click

from simplelogincmd.cli import const, util


@click.command(
    "list",
    short_help=const.HELP.ALIAS.LIST.SHORT,
    help=const.HELP.ALIAS.LIST.LONG,
    epilog=const.HELP.ALIAS.LIST.EPILOG,
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.LIST.OPTION.EXCLUDE,
)
@click.option(
    "-p",
    "--pinned",
    "query",
    flag_value="pinned",
    help=const.HELP.ALIAS.LIST.OPTION.PINNED,
)
@click.option(
    "-n",
    "--enabled",
    "query",
    flag_value="enabled",
    help=const.HELP.ALIAS.LIST.OPTION.ENABLED,
)
@click.option(
    "-d",
    "--disabled",
    "query",
    flag_value="disabled",
    help=const.HELP.ALIAS.LIST.OPTION.DISABLED,
)
@click.pass_obj
@util.authenticate
def list(obj, include: str | None, exclude: str | None, query: str | None) -> None:
    """Display aliases in a tabular format"""
    sl, db, cfg = obj.sl, obj.db, obj.cfg
    fields = util.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    aliases = sl.get_all_aliases(query)
    if len(aliases) == 0:
        click.echo("No aliases found.")
        return
    for alias in aliases:
        db.session.upsert(alias)
    db.session.commit()
    pager_threshold = cfg.get("display.pager-threshold")
    util.display_model_list(aliases, fields, pager_threshold)
