"""
Project-wide constants
"""

from pathlib import Path

from click import get_app_dir


APP_NAME = "SimpleLogin-CLI"

DIR_ROOT = Path(__file__).parent.parent
DIR_APPDATA = Path(get_app_dir(APP_NAME))
FILE_CONFIG = DIR_APPDATA / "config.ini"
FILE_DB = DIR_APPDATA / "db.sqlite"


CONFIG_DEFAULT = dict(
    API=dict(),
)
