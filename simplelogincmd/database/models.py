"""
SimpleLogin object models
"""

from typing import Any

from sqlalchemy import (
    Select,
    inspect,
    select,
)
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
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

    def __eq__(self, other) -> bool:
        return type(self) is type(other) and self.id == other.id

    @classmethod
    def identifier_query(cls, query: Select, id: Any) -> Select:
        """
        Restrict a query based on a generic identifier

        In the event that `id` is not a numeric primary key id, model
        classes can decide for themselves, by overriding this method,
        how to find the objects to which `id` refers. Overriding
        implementations should restrict `query`, as via a call to
        :meth:`sqlalchemy.Select.where` or similar, to a condition that
        identifies one (ideally) or more objects. For example, a
        Mailbox model might allow to search through email addresses,
        while an Alias model might search emails and alias notes for
        a match.

        :param query: The query to be conditioned
        :type query: :class:`sqlalchemy.Select`
        :param id: The identifier which is supposed to identify ideally
            one, but potentialy many or no model objects
        :type id: Any

        :return: The modified query
        :rtype: :class:`sqlalchemy.Select`
        """
        return query

    @classmethod
    def resolve_identifier(cls, session: Session, id: Any) -> list["Object"]:
        """
        Retrieve a list of model objects based on a generic identifier

        Attempt to produce a single model object by passing `id`
        directly on to :meth:`sqlalchemy.orm.Session.get_one`. If
        that fails, then fall back to
        :meth:`~simplelogincmd.database.models.identifier_query`, which
        subclasses can override in order to determine how that
        particular model should interpret the identifier.

        :param session: The database session which is to search for
            object(s)
        :type session: :class:`sqlalchemy.orm.Session`
        :param id: The identifier for which to search. This might be
            as simple as a primary key numeric id, or it could be a
            string which (ideally uniquely) identifies a particular
            model object.
        :type id: Any

        :return: A list of zero or more matching model objects
        :rtype: list[Object]
        """
        try:
            return [session.get_one(cls, id)]
        # Catch bad `id` value as well as no result found.
        except InvalidRequestError:
            query = select(cls)
            query = cls.identifier_query(query, id)
            return session.scalars(query).all()

    def get(self, field: str) -> str | None:
        """
        Retrieve the value of the given field

        :param field: The name of the field to get
        :type field: str

        :return: The field's value, or None if the field is undefined
        :rtype: str | None
        """
        return getattr(self, field, None)

    def get_string(self, field: str) -> str:
        """
        Retrieve a string representation of the field

        :param field: The name of the field to get
        :type field: str

        :return: String representation of the field's value

            - if value is string, then return value
            - if value is None, then ""
            - if value is bool, then "Y" or "N"
            - if value is iterable, then each element as a string,
              separated by commas
            - otherwise return str(value)

        :rtype: str
        """
        value = self.get(field)
        if isinstance(value, str):
            return value
        if value is None:
            return ""
        if isinstance(value, bool):
            return "Y" if value else "N"
        if not isinstance(value, dict):
            try:
                return ", ".join(str(elem) for elem in value)
            except TypeError:
                pass
        return str(value)


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

    @classmethod
    def identifier_query(cls, query: Select, id: Any) -> Select:
        like_string = f"%{id}%"
        email_like = cls.email.ilike(like_string)
        return query.where(email_like)


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
        if (mailboxes := extras.get("mailboxes")) is not None:
            self.mailboxes = [Mailbox(**mailbox) for mailbox in mailboxes]

    def __str__(self) -> str:
        return self.email

    @classmethod
    def identifier_query(cls, query: Select, id: Any) -> Select:
        like_string = f"%{id}%"
        email_like = cls.email.ilike(like_string)
        note_like = cls.note.ilike(like_string)
        condition = email_like | note_like
        return query.where(condition)


class Contact(LenientInit, Object):
    """
    An alias contact
    """

    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    contact: Mapped[str]
    reverse_alias: Mapped[str]
    reverse_alias_address: Mapped[str]
    block_forward: Mapped[bool]
    last_email_sent_timestamp: Mapped[int] = mapped_column(nullable=True)
    creation_timestamp: Mapped[int]

    def __init__(self, **kwargs) -> None:
        self._lenient_init(**kwargs)

    def __str__(self) -> str:
        return self.contact  # email address

    @classmethod
    def identifier_query(cls, query: Select, id: Any) -> Select:
        like_string = f"%{id}%"
        email_like = cls.contact.ilike(like_string)
        return query.where(email_like)


class Activity(LenientInit, Object):
    """
    An alias activity
    """

    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str]
    sender: Mapped[str]
    recipient: Mapped[str]
    reverse_alias: Mapped[str]
    reverse_alias_address: Mapped[str]
    timestamp: Mapped[int]

    def __init__(self, **kwargs):
        # SimpleLogin API sends "from" and "to" keys. Rename these to
        # avoid problems.
        if kwargs.get("sender") is None:
            kwargs["sender"] = kwargs.get("from")
        if kwargs.get("recipient") is None:
            kwargs["recipient"] = kwargs.get("to")
        self._lenient_init(**kwargs)

    def __str__(self) -> str:
        return self.action

    @classmethod
    def identifier_query(cls, query: Select, id: Any) -> Select:
        like_string = f"%{id}%"
        sender_like = cls.sender.ilike(like_string)
        recipient_like = cls.recipient.ilike(like_string)
        condition = sender_like | recipient_like
        return query.where(condition)
