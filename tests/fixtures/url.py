from urllib.parse import urljoin

import pytest

from simplelogincmd.rest import const


@pytest.fixture(scope="session")
def url_base():
    return const.BASE_URL


@pytest.fixture(scope="session")
def url_login(url_base):
    return urljoin(url_base, const.ENDPOINT.LOGIN)


@pytest.fixture(scope="session")
def url_mfa(url_base):
    return urljoin(url_base, const.ENDPOINT.MFA)


@pytest.fixture(scope="session")
def url_logout(url_base):
    return urljoin(url_base, const.ENDPOINT.LOGOUT)


@pytest.fixture(scope="session")
def url_mailboxes(url_base):
    return urljoin(url_base, const.ENDPOINT.MAILBOXES)


@pytest.fixture(scope="session")
def url_alias_options(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS_OPTIONS)


@pytest.fixture(scope="session")
def url_alias_custom(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS_CUSTOM)


@pytest.fixture(scope="session")
def url_alias_random(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS_RANDOM)


@pytest.fixture(scope="session")
def url_aliases(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIASES)


@pytest.fixture(scope="session")
def url_alias(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS)


@pytest.fixture(scope="session")
def url_alias_toggle(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS_TOGGLE)


@pytest.fixture(scope="session")
def url_alias_activities(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS_ACTIVITIES)


@pytest.fixture(scope="session")
def url_alias_contacts(url_base):
    return urljoin(url_base, const.ENDPOINT.ALIAS_CONTACTS)
