"""
Module for handling application configuration
"""

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import ValidationError
from jsonschema.validators import validator_for

from simplelogincmd import const


class Config:
    """
    Manage application configuration
    """

    def __init__(
        self,
        user_config_path: Path | None = None,
        base_obj: dict | None = None,
        schema_obj: dict | None = None,
    ) -> None:
        """
        Constructor

        Construct a complete configuration given a base set, a user-
        specific set that is merged into the base, and a JSON schema
        that validates both, as well as any attempts to modify values
        after initialization.

        Assuming both the user config file and the base config object
        pass validation, the final full configuration will be the base
        config, plus any values defined in the user config. Further,
        any values defined in both sets resolve to those in the user
        config.

        If the user configuration fails validation, merging is quietly
        not performed. That is, the final configuration will be the
        same as the base config with no modifications. This is also
        the case when reading the file fails due either to an OS error
        or a JSON decoding error.

        If the base configuration or the schema itself fail validation,
        exceptions are raised. This ensures that at least one valid
        configuration is available to the application.

        `base_obj` and `schema_obj` are deep-copied, so users can
        feel free to use them elsewhere without fear of modification
        by this class.

        :param user_config_path: Path to the user's configuration file,
            defaults to a path defined by the application
        :type user_config_path: :class:`pathlib.Path`, optional
        :param base_obj: The default configuration, defaults to the
            application's default config
        :type base_obj: dict
        :param schema_obj: The JSON schema that defines the structure
            of config files/objects, defaults to a schema defined by
            the application
        :type schema_obj: dict

        :raise jsonschema.ValidationError: If `base_obj` is invalid
            according to the schema
        :raise jsonschema.SchemaError: If the schema itself is invalid
        """
        schema = copy.deepcopy(schema_obj or const.CONFIG_SCHEMA)
        validator_cls = validator_for(schema)
        # This will raise if `schema` is invalid.
        validator_cls.check_schema(schema)
        validator = validator_cls(schema)

        base = copy.deepcopy(base_obj or const.CONFIG_BASE)
        # This will raise if `base` is invalid.
        validator.validate(base)

        path = user_config_path or const.FILE_CONFIG
        try:
            with path.open("r", encoding="utf-8") as config_file:
                config = json.load(config_file)
        except (OSError, json.JSONDecodeError):
            # TODO: Implement logging.
            config = {}
        try:
            validator.validate(config)
        except ValidationError:
            # TODO: Implement logging.
            config = {}

        self._validator = validator
        self._config = self._merge_configs(base, config)
        self._base = base
        self._schema = schema
        self._path = path
        self._cache = {}

    def _merge_configs(self, base: dict, config: dict) -> dict:
        """
        Merge a set of configurations together

        The result is a copy of `base`, where any values defined in
        `config` are added to or overwrite those defined in `base`.

        :param base: The base configuration
        :type base: dict
        :param config: The configuration to merge into `base`
        :type config: dict

        :rtype: dict
        """
        merged = copy.deepcopy(base)
        for k, v in config.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = self._merge_configs(merged[k], v)
            else:
                merged[k] = v
        return merged

    def _all(self, root: dict | None = None, path: str = "") -> dict:
        """
        Construct a set of all config keys with their values
        """
        root = root or self._config
        items = []
        for k, v in root.items():
            new_path = k if path == "" else f"{path}.{k}"
            if v and isinstance(v, dict):
                sub_items = self._all(v, new_path).items()
                items.extend(sub_items)
            else:
                sub_item = (new_path, v)
                items.append(sub_item)
        return dict(items)

    def validate(self, config) -> ValidationError | None:
        """
        Validate a configuration

        :param config: The configuration to validate
        :type config: dict

        :return: `None` if validation succeeds; otherwise, the
            ValidationError instance that was raised during validation
        :rtype: :class:`jsonschema.ValidationError`, optional
        """
        try:
            self._validator.validate(config)
        except ValidationError as error:
            return error

    def get(self, key: str) -> Any:
        """
        Retrieve a configuration value

        :param key: A dot-separated path from the config's root to the
            value desired (e.g., "api.api-key") to get the value of
            `api-key` under the `api` section.
        :type key: str

        :raise KeyError: If the given key leads to no value

        :return: The config value requested. If the given path leads
            to an object, return a deep copy of that object in order
            to prevent inadvertently making un-validated changes to
            the configuration
        :rtype: Any
        """
        if key in self._cache:
            return self._cache[key]
        node = self._config
        parts = key.split(".")
        for part in parts:
            try:
                node = node[part]
            except (KeyError, TypeError):
                raise KeyError(key) from None
        if isinstance(node, dict):
            # If we return this directly, it would be possible to
            # write new config values that bypass validation.
            node = copy.deepcopy(node)
        self._cache[key] = node
        return node

    def set(self, key: str, value: Any) -> str | None:
        """
        Attempt to modify a config setting

        If the config created by this modification fails to pass
        validation, no change is actually made, and an error message
        is produced.

        :param key: A dot-separated path from the config's root to the
            value desired (e.g., "api.api-key") to set the value of
            `api-key` under the `api` section.
        :type key: str
        :param value: The new value of the given setting
        :type value: Any

        :raise KeyError: If the given key leads to no value

        :return: A (mostly) human-readable error message if the config
            created by this modification is invalid; otherwise, `None`
        :rtype: str, optional
        """
        parts = key.split(".")
        # No check for IndexError because `parts` is at least `[""]`.
        last = parts.pop(-1)
        new = {}
        node = new
        for part in parts:
            node[part] = {}
            node = node[part]
        node[last] = value
        if (error := self.validate(new)) is not None:
            return f"{key}: {error.message}"
        self._config = self._merge_configs(self._config, new)
        self._cache[key] = value

    def restore(self) -> None:
        """
        Restore all configuration to their default values
        """
        self._cache = {}
        self._config = copy.deepcopy(self._base)

    def ensure_directory(self) -> bool:
        """
        Ensure that the parent directory of the config file exists

        Attempt to create it if it does not.

        :return: Whether the directory now exists
        :rtype: bool
        """
        directory = self._path.parent
        if directory.exists():
            return True
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError:
            return False
        directory.chmod(0o755)  # drwxr-xr-x
        return True

    def save(self) -> bool:
        """
        Save the configuration to a file

        :return: Whether the save succeeds
        :rtype: bool
        """
        if not self.ensure_directory():
            return False
        try:
            with self._path.open("w", encoding="utf-8") as file:
                json.dump(self._config, file, indent=4)
        except OSError:
            return False
        self._path.chmod(0o600)  # -rw-------
        return True

    def all(self) -> dict:
        """
        Construct a set of all configuration keys with their values
        """
        # Simple wrapper to hide the signature of the recursive method.
        return self._all()
