from sqlalchemy import text
from sqlalchemy_utils import database_exists


class TestDatabaseInitialization:

    def test_create_new_db(self, db_access):
        url = db_access.engine.url
        assert not database_exists(url)
        assert db_access.initialize()
        assert database_exists(url)

    def test_creation_when_db_file_already_exists_does_nothing(self, db_access):
        url = db_access.engine.url
        assert db_access.initialize()
        assert database_exists(url)
        assert db_access.initialize()
        assert database_exists(url)

    def test_db_file_has_readwrite_permissions_for_user_only(self, db_access):
        db_access.initialize()
        path = db_access.engine.path
        mode = path.stat().st_mode
        assert mode & 0o600 == 0o600

    def test_tables_are_created(self, db_access):
        # Test whether SELECTing from a table which should exist does
        # *not* raise any exception. No asserts are necessary. If the
        # tables are not created, then `execute` will raise and the
        # test will fail.
        db_access.initialize()
        tables = db_access.base.metadata.sorted_tables
        for table in tables:
            sql = text(f"SELECT * FROM {table.name};")
            db_access.session.execute(sql)


class TestDatabaseDestruction:

    def test_no_error_when_db_file_does_not_exist(self, db_access):
        assert db_access.destroy()
        assert not database_exists(db_access.engine.url)

    def test_remove_existing_db(self, db_access):
        url = db_access.engine.url
        db_access.initialize()
        assert database_exists(url)
        assert db_access.destroy()
        assert not database_exists(url)
