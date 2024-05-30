import pytest

from sqlalchemy import create_engine, URL

from simplelogincmd.database.access_layer import DatabaseAccessLayer


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
