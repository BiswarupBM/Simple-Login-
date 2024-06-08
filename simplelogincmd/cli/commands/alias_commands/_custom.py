import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Mailbox


def _custom(
    hostname,
    prefix,
    mailboxes,
    note,
    name,
    select_suffix,
    bypass_confirmation,
):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
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

    mailbox_ids = {input.resolve_id(db, Mailbox, mb_id) for mb_id in mailboxes}
    if note == "_EDIT":
        note = input.edit()

    # If `select_suffix` is not set or out of range, prompt the user
    # for which suffix to use.
    if (suffixes := data.get("suffixes")) is None:
        click.echo("Error retrieving alias suffixes")
        return False
    if select_suffix is None or not (0 <= select_suffix < len(suffixes)):
        options = [suffix["suffix"] for suffix in suffixes]
        suffix_index = input.prompt_choice("Choose a suffix", options)
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
