def cfg():
    """
    Initialize application configuration

    :raise jsonschema.SchemaError: If the app's configuration schema
        is invalid
    :raise jsonschema.ValidationError: If the app's base configuration
        fails validation

    :return: Application configuration
    :rtype: :class:`~simplelogincmd.config.Config`
    """
    from simplelogincmd.config import Config

    return Config()


def sl(cfg):
    """
    Initialize a SimpleLogin client

    The client is automatically logged in if an API key exists in the
    given configuration. If not, the user is prompted to log in.

    :param cfg: The application configuration used to configure this
        client
    :type cfg: :class:`~simplelogincmd.config.Config`

    :raise simplelogincmd.cli.exceptions.NotLoggedInError: If the user
        fails authentication

    :return: The configured SimpleLogin client, ready to make requests
    :rtype: :class:`SimpleLogin`
    """
    from simplelogincmd.rest import SimpleLogin

    sl = SimpleLogin()
    if api_key := cfg.get("api.api-key"):
        sl.api_key = api_key
        return sl

    import click

    from simplelogincmd.cli.commands.account.login import login
    from simplelogincmd.cli.exceptions import NotLoggedInError

    context = click.get_current_context()
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True)
    context.obj = sl
    success = context.invoke(login, email=email, password=password)
    if not success:
        raise NotLoggedInError()
    return sl


def db(cfg):
    """
    Initialize the database

    :param cfg: The Application configuration used to configure the
        db
    :type cfg: :class:`~simplelogincmd.config.Config`

    :rtype: :class:`~simplelogincmd.database.DatabaseAccessLayer`
    """
    from simplelogincmd.database import DatabaseAccessLayer

    db = DatabaseAccessLayer()
    cfg.ensure_directory()
    db.initialize()
    return db
