"""
Database-access-layer class module
"""

import os
from typing import Type

from sqlalchemy import (
    URL,
    Engine,
    create_engine,
)
from sqlalchemy.orm import Session
from sqlalchemy_utils import (
    create_database,
    database_exists,
    drop_database,
)

from simplelogincmd import const
from simplelogincmd.database.models import Object
from simplelogincmd.database.session import SimpleLoginSession


def _create_engine():
    """
    Create a database engine configured for the default application db
    """
    name = const.FILE_DB.as_posix()
    url = URL.create(drivername="sqlite+pysqlite", database=name)
    engine = create_engine(url)
    return engine


class DatabaseAccessLayer:
    """
    Proxy between database consumers and the database itself

    Ease testing, abstract away implementation details, and normalize
    database interaction by providing a single class whose instances
    contain everything necessary to manage the database and load,
    modify, and persist model objects.
    """

    def __init__(
        self,
        engine: Engine | None = None,
        declarative_base: Type | None = None,
        session_cls: Session | None = None,
    ) -> None:
        """
        Constructor

        :param engine: The SQLAlchemy engine which manages the db,
         defaults to an engine suited to the application
        :type engine: :class:`sqlalchemy.engine.Engine`, optional
        :param declarative_base: The base class of all other database
            model classes, defaults to a base configured for the
            application
        :type declarative_base: Type, subclass of
            :class:`sqlalchemy.orm.DeclarativeBase`, optional
        :param session_cls: The type of session to be used for
            interacting with the db, defaults to a session suitable to
            the application
        :type session_cls: Type, subclass of
            :class:`sqlalchemy.orm.session.Session`, optional
        """
        if engine is None:
            engine = _create_engine()
        if declarative_base is None:
            declarative_base = Object
        if session_cls is None:
            session_cls = SimpleLoginSession
        self.engine = engine
        self.base = declarative_base
        self.session = session_cls(self.engine)

    def initialize(self) -> bool:
        """
        Initialize the database if it does not already exist

        Create the database, as well as all its tables, if it does not
        already exist. If it does, do nothing.

        :return: Whether initialization succeeds
        :rtype: bool
        """
        url = self.engine.url
        if not database_exists(url):
            try:
                create_database(url)
            # TODO: Narrow this except to catch appropriate errors.
            # None are documented by sqlalchemy_utils.
            except Exception:
                return False
            os.chmod(url.database, 0o600)  # -rw-------
            self.base.metadata.create_all(self.engine)
        return True

    def destroy(self) -> bool:
        """
        Drop the entire database

        :return: Whether the destruction succeeds
        :rtype: bool
        """
        url = self.engine.url
        if database_exists(url):
            try:
                drop_database(url)
            # TODO: Narrow this except to catch appropriate errors.
            # None are documented by sqlalchemy_utils.
            except Exception:
                return False
            finally:
                # https://github.com/sqlalchemy/sqlalchemy/discussions/9188
                # Ensure that connections are closed, otherwise a
                # `OperationalError` with a rather misleading message
                # about writing to a read-only database can occur.
                self.engine.dispose()
        return True

    def clear(self) -> bool:
        """
        Drop and re-initialize the database

        Simple helper that calls :meth:`.destroy` and then, if that
        succeeds, "meth"`.initialize`.

        :return: Whether the entire process of destruction and
            re-initialization succeeds
        :rtype: bool
        """
        if self.destroy():
            return self.initialize()
        return False
