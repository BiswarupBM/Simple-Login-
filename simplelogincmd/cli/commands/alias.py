"""
CLI commands regarding SimpleLogin's alias endpoints

Subcommands:

- activity
- contact
    - create
    - list
- custom
- delete
- get
- list
- random
- toggle
- update
"""

import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


@click.group(
    "alias",
    short_help=const.HELP.ALIAS.SHORT,
    help=const.HELP.ALIAS.LONG,
)
@util.pass_simplelogin
@util.authenticate
def alias(sl):
    """Alias commands"""
    pass


@alias.command(
    "activity",
    short_help=const.HELP.ALIAS.ACTIVITY.SHORT,
    help=const.HELP.ALIAS.ACTIVITY.LONG,
    epilog=const.HELP.ALIAS.ACTIVITY.EPILOG,
)
@click.argument(
    "id",
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.ACTIVITY.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.ACTIVITY.OPTION.EXCLUDE,
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def activity(sl, db, id: int, include: str | None, exclude: str | None) -> None:
    """Display alias activities in a tabular format"""
    fields = util.get_display_fields_from_options(
        const.ACTIVITY_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    id = util.resolve_id(db, Alias, id)
    activities = sl.get_all_alias_activities(id)
    if len(activities) == 0:
        click.echo("No activities found")
        return
    util.display_model_list(activities, fields)


@alias.command(
    "custom",
    short_help=const.HELP.ALIAS.CUSTOM.SHORT,
    help=const.HELP.ALIAS.CUSTOM.LONG,
)
@click.option(
    "-o",
    "--hostname",
    help=const.HELP.ALIAS.CUSTOM.OPTION.HOSTNAME,
)
@click.option(
    "-p",
    "--prefix",
    help=const.HELP.ALIAS.CUSTOM.OPTION.PREFIX,
)
@click.option(
    "-m",
    "--mailbox",
    "mailboxes",
    required=True,
    multiple=True,
    help=const.HELP.ALIAS.CUSTOM.OPTION.MAILBOXES,
)
@click.option(
    "-n",
    "--note",
    is_flag=False,
    flag_value="_EDIT",
    help=const.HELP.ALIAS.CUSTOM.OPTION.NOTE,
)
@click.option(
    "-a",
    "--name",
    help=const.HELP.ALIAS.CUSTOM.OPTION.NAME,
)
@click.option(
    "-s",
    "--select-suffix",
    type=int,
    help=const.HELP.ALIAS.CUSTOM.OPTION.SELECT_SUFFIX,
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirmation",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.ALIAS.CUSTOM.OPTION.YES,
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def custom(
    sl,
    db,
    hostname: str | None,
    prefix: str,
    mailboxes: tuple[str],
    note: str | None,
    name: str | None,
    select_suffix: int | None,
    bypass_confirmation: bool,
) -> bool:
    """Create a new custom alias"""
    # Get suffix, recommendation, and other info before creating anything.
    success, data = sl.get_alias_options(hostname)
    if not success:
        click.echo(data)
        return False
    if not data.get("can_create"):
        click.echo("You are unable to create custom aliases.")
        return False

    # If there is a recommendation, display it and confirm that the user
    # still wants to create a new alias, unless `bypass_confirmation`
    # is set.
    if (recommendation := data.get("recommendation")) is not None:
        rec_alias = recommendation.get("alias", "Another alias")
        rec_host = recommendation.get("hostname", "that site")
        click.echo(f"{rec_alias} has already been used on {rec_host}.")
        if not bypass_confirmation:
            click.confirm("Create a new alias anyway?", abort=True)

    mailbox_ids = {util.resolve_id(db, Mailbox, mb_id) for mb_id in mailboxes}
    if note == "_EDIT":
        note = util.edit()

    # If `select_suffix` is not set or out of range, prompt the user
    # for which suffix to use.
    if (suffixes := data.get("suffixes")) is None:
        click.echo("Error retrieving alias suffixes")
        return False
    if select_suffix is None or not (0 <= select_suffix < len(suffixes)):
        options = [suffix["suffix"] for suffix in suffixes]
        suffix_index = util.prompt_choice("Choose a suffix", options)
    else:
        suffix_index = select_suffix
    suffix = suffixes[suffix_index].get("suffix")
    signed_suffix = suffixes[suffix_index].get("signed_suffix")

    # If a prefix was not given, check for a prefix suggestion. If no
    # suggestion, then prompt for input. Otherwise, try to use the
    # suggestion.
    if prefix is None:
        prefix_suggestion = data.get("prefix_suggestion", "")
        if prefix_suggestion == "":
            # Cannot bypass this prompt because the prefix is required.
            prefix = click.prompt("Alias prefix")
        elif bypass_confirmation or click.confirm(
            f"Use {prefix_suggestion} for prefix?"
        ):
            prefix = prefix_suggestion
        else:
            # Cannot bypass this prompt because prefix is required.
            prefix = click.prompt("Alias prefix")

    if not bypass_confirmation:
        click.confirm(f"Create alias {prefix}{suffix}?", abort=True)

    # Finally, do the actual creation and display results.
    success, obj = sl.create_custom_alias(
        alias_prefix=prefix,
        signed_suffix=signed_suffix,
        mailbox_ids=mailbox_ids,
        note=note,
        name=name,
        hostname=hostname,
    )
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.email)
    return True


@alias.command(
    "get",
    short_help=const.HELP.ALIAS.GET.SHORT,
    help=const.HELP.ALIAS.GET.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.GET.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.GET.OPTION.EXCLUDE,
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def get(sl, db, id: int, include: str | None, exclude: str | None) -> None:
    """Display a single alias in a tabular format"""
    fields = util.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    id = util.resolve_id(db, Alias, id)
    success, obj = sl.get_alias(id)
    if not success:
        click.echo(obj)
        return None
    db.session.upsert(obj)
    db.session.commit()
    util.display_model_list([obj], fields, use_pager=False)


@alias.command(
    "delete",
    short_help=const.HELP.ALIAS.DELETE.SHORT,
    help=const.HELP.ALIAS.DELETE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirmation",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.ALIAS.DELETE.OPTION.YES,
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def delete(sl, db, id: int, bypass_confirmation: bool) -> bool:
    """Delete an alias"""
    id = util.resolve_id(db, Alias, id)
    if not bypass_confirmation:
        success, obj = sl.get_alias(id)
        if not success:
            # Clarify the somewhat vague error message for invalid ID
            msg = f"Unknown ID {id}" if "Unknown" in obj else obj
            click.echo(msg)
            return False
        click.confirm(f"Delete {obj.email}?", abort=True)
    success, msg = sl.delete_alias(id)
    if not success:
        # Clarify the somewhat vague error message
        msg = f"Unknown ID {id}" if msg == "Forbidden" else msg
        click.echo(msg)
        return False
    return True


@alias.command(
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
@util.pass_db_access
@util.pass_simplelogin
def list(sl, db, include: str | None, exclude: str | None, query: str | None) -> None:
    """Display aliases in a tabular format"""
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
    util.display_model_list(aliases, fields)


@alias.command(
    "random",
    short_help=const.HELP.ALIAS.RANDOM.SHORT,
    help=const.HELP.ALIAS.RANDOM.LONG,
    epilog=const.HELP.ALIAS.RANDOM.EPILOG,
)
@click.option(
    "-o",
    "--hostname",
    help=const.HELP.ALIAS.RANDOM.OPTION.HOSTNAME,
)
@click.option(
    "-u",
    "--uuid",
    "mode",
    flag_value="uuid",
    help=const.HELP.ALIAS.RANDOM.OPTION.UUID,
)
@click.option(
    "-w",
    "--word",
    "mode",
    flag_value="word",
    help=const.HELP.ALIAS.RANDOM.OPTION.WORD,
)
@click.option(
    "-n",
    "--note",
    is_flag=False,
    flag_value="_EDIT",
    help=const.HELP.ALIAS.RANDOM.OPTION.NOTE,
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def random(
    sl,
    db,
    hostname: str | None,
    mode: str | None,
    note: str | None,
) -> bool:
    """Create a new random alias"""
    if note == "_EDIT":
        note = util.edit()
    success, obj = sl.create_random_alias(hostname, mode, note)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.email)
    return True


@alias.command(
    "toggle",
    short_help=const.HELP.ALIAS.TOGGLE.SHORT,
    help=const.HELP.ALIAS.TOGGLE.LONG,
)
@click.argument(
    "id",
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def toggle(sl, db, id: int) -> bool:
    """Enable or disable an alias"""
    id = util.resolve_id(db, Alias, id)
    success, result = sl.toggle_alias(id)
    if not success:
        click.echo(result)
        return False
    click.echo("Enabled" if result else "Disabled")
    return True


@alias.command(
    "update",
    short_help=const.HELP.ALIAS.UPDATE.SHORT,
    help=const.HELP.ALIAS.UPDATE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-n",
    "--note",
    is_flag=False,
    flag_value="_EDIT",
    help=const.HELP.ALIAS.UPDATE.OPTION.NOTE,
)
@click.option(
    "-a",
    "--name",
    help=const.HELP.ALIAS.UPDATE.OPTION.NAME,
)
@click.option(
    "-m",
    "--mailbox",
    "mailboxes",
    required=True,
    multiple=True,
    help=const.HELP.ALIAS.UPDATE.OPTION.MAILBOXES,
)
@click.option(
    "-d/-D",
    "--disable-pgp/--no-disable-pgp",
    default=None,
    help=const.HELP.ALIAS.UPDATE.OPTION.DISABLE_PGP,
)
@click.option(
    "-p/-P",
    "--pinned/--no-pinned",
    default=None,
    help=const.HELP.ALIAS.UPDATE.OPTION.PINNED,
)
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def update(
    sl,
    db,
    id: int,
    note: str | None,
    name: str | None,
    mailboxes: tuple[str],
    disable_pgp: bool | None,
    pinned: bool | None,
) -> bool:
    """Modify an alias's fields"""
    id = util.resolve_id(db, Alias, id)
    mailbox_ids = {util.resolve_id(db, Mailbox, mb_id) for mb_id in mailboxes}
    if note == "_EDIT":
        note = util.edit()
    success, msg = sl.update_alias(
        alias_id=id,
        note=note,
        name=name,
        mailbox_ids=mailbox_ids,
        disable_pgp=disable_pgp,
        pinned=pinned,
    )
    if not success:
        click.echo(msg)
        return False
    return True


@click.group(
    "contact",
    short_help=const.HELP.ALIAS.CONTACT.SHORT,
    help=const.HELP.ALIAS.CONTACT.LONG,
)
@util.pass_simplelogin
@util.authenticate
def _contact(sl):
    """Contact commands"""
    pass


@_contact.command(
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
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def contact_create(sl, db, id: int, email: str) -> bool:
    """Create a new contact"""
    id = util.resolve_id(db, Alias, id)
    success, obj = sl.create_contact(id, email)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.reverse_alias_address)
    return True


@_contact.command(
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
@util.pass_db_access
@util.pass_simplelogin
@util.authenticate
def contact_list(sl, db, id: int, include: str | None, exclude: str | None) -> None:
    """List contacts in a tabular format"""
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
    util.display_model_list(contacts, fields)


alias.add_command(_contact)
