import json

import jsonschema
import pytest

from simplelogincmd.config import Config


@pytest.fixture
def config(tmp_config_file, base, schema):
    return Config(tmp_config_file, base, schema)


class TestInit:

    def test_invalid_schema_raises_error(self, tmp_config_file, base, schema_invalid):
        with pytest.raises(jsonschema.SchemaError):
            Config(tmp_config_file, base, schema_invalid)

    def test_invalid_base_raises_error(self, tmp_config_file, base_invalid, schema):
        with pytest.raises(jsonschema.ValidationError):
            Config(tmp_config_file, base_invalid, schema)

    def test_invalid_user_is_not_merged(
        self, tmp_config_file, user_invalid, base, schema
    ):
        tmp_config_file.parent.mkdir()
        with tmp_config_file.open("w", encoding="utf-8") as file:
            json.dump(user_invalid, file, indent=4)
        cfg = Config(tmp_config_file, base, schema)
        assert cfg.get("api.api-key") != user_invalid["api"]["api-key"]
        assert cfg.get("api.api-key") == base["api"]["api-key"]
        assert cfg.get("test.int") != user_invalid["test"]["int"]
        assert cfg.get("test.int") == base["test"]["int"]

    def test_valid_user_is_merged(self, tmp_config_file, user, base, schema):
        tmp_config_file.parent.mkdir()
        with tmp_config_file.open("w", encoding="utf-8") as file:
            json.dump(user, file, indent=4)
        cfg = Config(tmp_config_file, base, schema)
        assert cfg.get("api.api-key") == user["api"]["api-key"]
        assert cfg.get("api.api-key") != base["api"]["api-key"]
        assert cfg.get("test.int") == user["test"]["int"]
        assert cfg.get("test.int") != base["test"]["int"]

    def test_new_config_has_no_api_key(self, config):
        assert config.get("api.api-key") == ""


class TestGet:

    def test_empty_key_raises(self, config):
        with pytest.raises(KeyError):
            config.get("")

    def test_undotted_invalid_key_raises(self, config):
        with pytest.raises(KeyError):
            config.get("nonexistentkey")

    def test_undotted_valid_key_returns_dict_copy(self, config):
        value = config.get("api")
        assert value is not config._config["api"]

    def test_get_dotted_invalid_key_raises(self, config):
        with pytest.raises(KeyError):
            config.get("not.a.valid.key")

    def test_valid_key_returns_value(self, config):
        assert config.get("api.api-key") == ""
        assert config.get("test.int") == 1


class TestSet:

    def test_empty_key_returns_error(self, config):
        assert config.set("", 1) is not None

    def test_invalid_key_returns_error(self, config):
        assert config.set("invalid.key", 1) is not None

    def test_invalid_value_returns_error(self, config):
        assert config.set("test.int", "bad value") is not None

    def test_valid_value_is_set(self, config):
        assert config.set("test.int", 42) is None
        assert config.get("test.int") == 42


class TestEnsureDirectory:

    def test_create_new_app_dir(self, tmp_config_file, config):
        assert not tmp_config_file.parent.exists()
        assert config.ensure_directory()
        assert tmp_config_file.parent.exists()

    def test_find_existing_app_dir(self, tmp_config_file, config):
        tmp_config_file.parent.mkdir()
        assert config.ensure_directory()

    def test_dir_has_correct_permissions(self, tmp_config_file, config):
        config.ensure_directory()
        mode = tmp_config_file.parent.stat().st_mode
        assert mode & 0o755 == 0o755


class TestSave:

    def test_saved_file_has_correct_permissions(self, tmp_config_file, config):
        assert config.save()
        mode = tmp_config_file.stat().st_mode
        assert mode & 0o600 == 0o600

    def test_saved_file_merges_on_next_init(
        self, config, tmp_config_file, base, schema
    ):
        config.set("api.api-key", "newsecretkey")
        config.save()
        cfg = Config(tmp_config_file, base, schema)
        assert cfg.get("api.api-key") == "newsecretkey"
