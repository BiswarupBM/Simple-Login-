import pytest
from sqlalchemy import URL, create_engine

from simplelogincmd.database.access_layer import DatabaseAccessLayer
from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


@pytest.fixture(scope="session")
def db_engine(tmp_path_factory):
    """
    Create a db engine bound to a temp directory

    The engine is given an extra attribute, `path`, which is an instance
    of :class:`pathlib.Path` that points to the engine's database URL.
    """
    path = tmp_path_factory.mktemp("db") / "db.sqlite"
    url = URL.create(drivername="sqlite+pysqlite", database=path.as_posix())
    engine = create_engine(url)
    # Make it easier to manipulate db file within tests/fixtures.
    setattr(engine, "path", path)
    return engine


@pytest.fixture
def db_access(db_engine):
    """
    A DatabaseAccessLayer bound to a testing db engine

    This fixture also cleans up db files on teardown.
    """
    access = DatabaseAccessLayer(engine=db_engine)
    yield access
    access.destroy()


@pytest.fixture
def mailbox():
    return Mailbox(
        id=1,
        email="test@site.com",
        nb_alias=0,
        verified=True,
        default=False,
        creation_timestamp=1,
    )


@pytest.fixture
def alias():
    return Alias(
        id=1,
        email="alias@sl.com",
        note="testing",
        nb_block=0,
        nb_forward=1,
        nb_reply=0,
        enabled=True,
        support_pgp=True,
        disable_pgp=False,
        pinned=False,
        creation_timestamp=1,
    )


@pytest.fixture
def complex_mailbox():
    mb = Mailbox(
        id=2,
        email="more@tests.io",
        nb_alias=5,
        verified=True,
        default=False,
        creation_timestamp=123,
    )
    setattr(mb, "list_attr", [1, 2, 3])
    setattr(mb, "dict_attr", {"key": "value"})
    return mb


@pytest.fixture
def ready_db(db_access):
    db_access.initialize()


@pytest.fixture
def populated_db(ready_db, db_access, alias, mailbox, complex_mailbox):
    db_access.session.add_all([alias, mailbox, complex_mailbox])
    db_access.session.commit()
