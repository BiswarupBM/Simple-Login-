import pytest


@pytest.fixture(scope="session")
def username():
    return "Tester"


@pytest.fixture(scope="session")
def email():
    return "test@email.com"


@pytest.fixture(scope="session")
def password():
    return "secretpassword"


@pytest.fixture(scope="session")
def api_key():
    return "supersecrettestapiapikey"


@pytest.fixture(scope="session")
def mfa_key():
    return "supersecrettestmfakey"


@pytest.fixture(scope="session")
def mfa_token():
    return 123456
