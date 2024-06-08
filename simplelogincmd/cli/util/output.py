import click


def get_display_fields_from_options(
    valid_fields: list[str],
    inclusions: str | None,
    exclusions: str | None,
) -> list[str]:
    """
    Make a list of valid fields based on which should be included and excluded

    Produce a list consisting of the valid items in `inclusions` (or
    those in `valid_fields` itself, if `inclusions` is empty), except
    for those found in `exclusions`. Comparisons are case-insensitive.

    :param valid_fields: All the possible valid fields
    :type valid_fields: list[str]
    :param inclusions: A comma-separated list of fields to be included.
        If empty, then assume all of `valid_fields` are to be included.
        Otherwise, include only the valid fields found in this list
    :type inclusions: str
    :param exclusions: Exclude any valid fields in this comma-separated
        list from the result
    :type exclusions: str

    :return: The valid fields as requested
    :rtype: list[str], might be empty
    """
    if inclusions is not None:
        inclusions = inclusions.lower()
        inclusions = inclusions.replace(" ", "")
        inclusions = inclusions.split(",")
        fields = [field for field in valid_fields if field in inclusions]
    else:
        fields = [field for field in valid_fields]
    if exclusions is not None:
        exclusions = exclusions.lower()
        exclusions = exclusions.replace(" ", "")
        exclusions = exclusions.split(",")
        fields = [field for field in fields if field not in exclusions]
    return fields


def _generate_model_list(models: list, fields: list[str]):
    """
    Generate a table displaying the given fields of each item

    :param models: List of :class:`~simplelogincmd.database.model.Object`
        to be included in the table
    :type models: list[Object]
    :param fields: The field names to be shown for each item
    :type fields: list[str]

    :return: A generator of each line of the table, including a heading
    :rtype: Generator
    """
    if len(models) == 0:
        return
    header = "|".join(fields)
    yield f"{header}\n"
    for model in models:
        properties = [model.get_string(field) for field in fields]
        entry = "|".join(properties)
        yield f"{entry}\n"


def display_model_list(
    models: list,
    fields: list[str],
    pager_threshold: int,
) -> None:
    """
    Print a simple table detailing each item to stdout

    :param models: Series of :class:`~simplelogincmd.database.models.Object`
        to be included in the output
    :type models: list[Object]
    :param fields: The field names to display for each item, in left-
        to-right order
    :type fields: list[str]
    :param pager_threshold: Display the items via a pager if the output
        consists of this many or more entries, including the heading.
        A value of `0` indicates not to use the pager.
    :type use_pager: int

    :rtype: None
    """
    count = len(models)
    if count == 0:
        return
    table = _generate_model_list(models, fields)
    # +1 to account for the heading.
    if 0 < pager_threshold <= count + 1:
        click.echo_via_pager(table)
        return
    for entry in table:
        # Entries come with newline appended, so suppress them here
        click.echo(entry, nl=False)
