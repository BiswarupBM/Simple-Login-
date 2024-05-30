"""
SimpleLogin object models
"""

from typing import Any

from sqlalchemy import (
    inspect,
    select,
    Select,
)
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)


class LenientInit:
    """
    Mixin class that provides a lenient model object constructor

    Usually, the model object constructor raises :exc:TypeError when
    it receives invalid keyword arguments. This lenient constructor
    simply ensures that no invalid keyword arguments are given to the
    default constructor, and returns any invalid arguments back to the
    caller for processing.

    Subclasses can have `__init__` methods like this::

        def __init__(self, **kwargs):
            extra_kwargs = self._lenient_init(**kwargs)
            # Do something with the rest of the keyword args.
    """

    def _lenient_init(self, **kwargs) -> dict:
        """
        Initialize `self` with valid arguments only

        Remaining arguments are returned unchanged.

        :rtype: dict
        """
        cls = type(self)
        mapper = inspect(cls)
        attrs = [attr.key for attr in mapper.attrs]
        valid = {attr: kwargs.pop(attr, None) for attr in attrs}
        super().__init__(**valid)
        return kwargs


class Object(DeclarativeBase):
    """
    Base class of all other SimpleLogin objects
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"


class Mailbox(LenientInit, Object):
    """
    A SimpleLogin mailbox
    """

    __tablename__ = "mailbox"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    nb_alias: Mapped[int]
    verified: Mapped[bool]
    default: Mapped[bool]
    creation_timestamp: Mapped[int]

    def __init__(self, **kwargs) -> None:
        self._lenient_init(**kwargs)

    def __str__(self) -> str:
        return self.email


class Alias(LenientInit, Object):
    """
    A SimpleLogin alias
    """

    __tablename__ = "alias"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    note: Mapped[str] = mapped_column(nullable=True)
    nb_block: Mapped[int]
    nb_forward: Mapped[int]
    nb_reply: Mapped[int]
    enabled: Mapped[bool]
    support_pgp: Mapped[bool]
    disable_pgp: Mapped[bool]
    pinned: Mapped[bool]
    creation_timestamp: Mapped[int]

    def __init__(self, **kwargs) -> None:
        extras = self._lenient_init(**kwargs)
        # N.b.: Mailboxes created here will always be transient and
        # never saved to the DB unless explicitly managed elsewhere.
        # They are created here because the SimpleLogin API provides
        # `id` and `email` attributes of each mailbox to which an
        # alias belongs, but they are never to be used beyond displaying
        # to the user.
        # This will never cause problems for SQLAlchemy because it loads
        # objects from the DB via a different method.
        if (mailboxes := kwargs.get("mailboxes")) is not None:
            self.mailboxes = [Mailbox(**mailbox) for mailbox in mailboxes]

    def __str__(self) -> str:
        return self.email
