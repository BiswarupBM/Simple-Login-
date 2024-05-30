"""
Module for handling application configuration
"""

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

from simplelogincmd import const


def default() -> dict:
    """
    Get default config

    :return: Application's default configuration
    :rtype: dict
    """
    return const.CONFIG_DEFAULT


def ensure_directory(path: Path | None = None) -> bool:
    """
    Create a config directory if it does not already exist

    :param path: The directory to check, defaults to the application's
        default config directory
    :type path: :class:`pathlib.Path`

    :return: Whether the directory now exists
    :rtype: bool
    """
    path = path or const.DIR_APPDATA
    if path.exists():
        return True
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        # TODO: Add logging / other notification mechanisms.
        return False
    path.chmod(0o755)  # drwxr-xr-x
    return True


def load(path: Path | None = None) -> ConfigParser:
    """
    Read configuration from a config file

    The config is first populated with default configuration as returned
    by :func:`default`, and then the given path (or the application's
    default config file, if none is given) is read in. Thus, no
    KeyErrors should occur when reading data from this configuration,
    as long as keys are present in at least the application's default
    config.

    :param path: The path of the configuration file to read, defaults
        to None
    :type path: :class:`pathlib.Path`, optional

    :return: Configuration
    :rtype: :class:`ConfigParser`
    """
    path = path or const.FILE_CONFIG
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read_dict(default())
    if len(config.read(path)) == 0:
        # TODO: Add logging / other notification mechanisms.
        pass
    return config


def save(config: ConfigParser, path: Path | None = None) -> bool:
    """
    Save the given configuration to disc

    If `path` is not given, the application's default config file path
    is used. Attempts are made to ensure that all directories along the
    path are created if they do not already exist so that callers need
    not handle this themselves.

    :param config: The configuration to save
    :type config: :class:`configparser.ConfigParser`
    :param path: Path to the file in which to write the data, defaults
        to None
    :type path: :class:`pathlib.Path`, optional

    :return: Whether the configuration saved successfully
    :rtype: bool
    """
    path = path or const.FILE_CONFIG
    directory = path.parent
    if not ensure_directory(directory):
        return False
    try:
        with path.open("w", encoding="utf-8") as file:
            config.write(file)
    except OSError:
        # TODO: Add logging / other notification mechanisms.
        return False
    path.chmod(0o600)  # -rw-------
    return True
