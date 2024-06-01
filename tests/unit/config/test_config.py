import pytest

from simplelogincmd import config


@pytest.fixture
def tmp_config_file(tmp_app_dir):
    """
    Construct a path to app's config file, but do not actually create it
    """
    return tmp_app_dir / "config.ini"


@pytest.fixture(autouse=True)
def monkey_app_dir(monkey, tmp_app_dir):
    """
    Replace app's app directory with a temp path
    """
    monkey.setattr("simplelogincmd.const.DIR_APPDATA", tmp_app_dir)


@pytest.fixture(autouse=True)
def monkey_config_file(monkey, tmp_config_file):
    """
    Replace app's config file path with a temp path
    """
    monkey.setattr("simplelogincmd.const.FILE_CONFIG", tmp_config_file)


def test_create_new_app_dir(tmp_app_dir):
    assert not tmp_app_dir.exists()
    assert config.ensure_directory()
    assert tmp_app_dir.exists()


def test_create_new_app_dir_in_specified_location(tmp_appdata_dir):
    custom_dir = tmp_appdata_dir / "custom"
    assert not custom_dir.exists()
    config.ensure_directory(custom_dir)
    assert custom_dir.exists()


def test_find_existing_app_dir(tmp_app_dir):
    tmp_app_dir.mkdir()
    assert config.ensure_directory()


def test_app_dir_has_correct_permissions(tmp_app_dir):
    config.ensure_directory()
    mode = tmp_app_dir.stat().st_mode
    assert mode & 0o755 == 0o755


def test_new_config_has_no_api_key():
    cfg = config.load()
    assert cfg["API"].get("api_key") is None


def test_saving_config_writes_to_file():
    cfg = config.load()
    cfg["API"]["api_key"] = "foobar"
    config.save(cfg)
    cfg = config.load()
    assert cfg["API"].get("api_key") == "foobar"
