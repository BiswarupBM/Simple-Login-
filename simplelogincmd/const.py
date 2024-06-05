"""
Project-wide constants
"""

from pathlib import Path

from click import get_app_dir


APP_NAME = "SimpleLogin-CLI"

DIR_ROOT = Path(__file__).parent.parent
DIR_APPDATA = Path(get_app_dir(APP_NAME))
FILE_CONFIG = DIR_APPDATA / "config.json"
FILE_DB = DIR_APPDATA / "db.sqlite"


CONFIG_SCHEMA = {
    "title": "SimpleLogin-CLI Configuration",
    "description": "The structure of an application config file for SimpleLogin-CLI",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "api": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "api-key": {
                    "type": "string",
                },
            },
        },
        "display": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "pager-threshold": {
                    "type": "integer",
                    "minimum": 0,
                },
            },
        },
    },
}

CONFIG_BASE = {
    "api": {
        "api-key": "",
    },
    "display": {
        "pager-threshold": 20,
    },
}
