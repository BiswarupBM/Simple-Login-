import pytest

from simplelogincmd.config import Config


@pytest.fixture
def tmp_config_file(tmp_app_dir):
    """
    Construct a path to app's config file, but do not actually create it
    """
    return tmp_app_dir / "config.json"


@pytest.fixture
def schema():
    return {
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
            "test": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "int": {
                        "type": "integer",
                        "minimum": 0,
                    },
                },
            },
        },
    }


@pytest.fixture
def schema_invalid(schema):
    schema["type"] = "invalid"
    return schema


@pytest.fixture
def base():
    return {
        "api": {
            "api-key": "",
        },
        "test": {
            "int": 1,
        },
    }


@pytest.fixture
def base_invalid(base):
    base["api"]["api-key"] = 69
    base["test"]["int"] = "invalid"
    return base


@pytest.fixture
def user():
    return {
        "api": {
            "api-key": "supersecret",
        },
        "test": {
            "int": 10,
        },
    }


@pytest.fixture
def user_invalid(user):
    user["api"]["api-key"] = 69
    user["test"]["int"] = "invalid"
    return user


@pytest.fixture
def config(tmp_config_file):
    return Config(tmp_config_file)
