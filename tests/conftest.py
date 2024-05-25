import importlib.util
from pkgutil import iter_modules

import pytest
from responses import Response

from simplelogincmd.rest import SimpleLogin

from . import fixtures


# The below was adapted for Python 3.12 from
# https://github.com/pytest-dev/pytest/issues/3582#issuecomment-402611178
# This is done so that fixtures can be separated into modules for easier
# navigation and understanding.
for finder, name, is_pkg in iter_modules(
    fixtures.__path__, prefix=f"{fixtures.__name__}."
):
    spec = importlib.util.find_spec(name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals().update({k: v for k, v in vars(module).items() if not k.startswith("_")})


@pytest.fixture
def sl_unauthenticated():
    return SimpleLogin()


@pytest.fixture
def sl(sl_unauthenticated, api_key):
    sl_unauthenticated._api_key = api_key
    return sl_unauthenticated
