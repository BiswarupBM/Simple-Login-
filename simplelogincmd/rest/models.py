"""
Models returned by the SimpleLogin API
"""


class Object:
    """A generic SimpleLogin object"""

    def __init__(self, *, id: int = None) -> None:
        """
        Constructor

        :param id: Object's numeric ID, defaults to None
        :type id: int, optional
        """
        self.id = id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.id == other.id

    def get(self, field: str) -> str | None:
        """
        Retrieve the value of the given field

        :param field: The name of the field to get
        :type field: str

        :return: The field's value, or None if the field is undefined
        :rtype: str | None
        """
        return getattr(self, field, None)

    def field_as_string(self, field: str) -> str:
        """
        Retrieve a string representation of the field

        :param field: The name of the field to get
        :type field: str

        :return: String representation of the field's value

            - if value is string, then return value
            - if value is None, then ""
            - if value is bool, then return "Y" or "N"
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
                return ",".join(str(elem) for elem in value)
            except TypeError:
                pass
        return str(value)


class Mailbox(Object):
    """A SimpleLogin mailbox"""

    def __init__(
        self,
        *,
        id: int | None = None,
        email: str | None = None,
        default: bool | None = None,
        creation_timestamp: int | None = None,
        nb_alias: int | None = None,
        verified: bool | None = None,
    ) -> None:
        """
        Constructor

        See SimpleLogin documentation for an explanation of the
        possible fields.
        """
        super().__init__(id=id)
        self.email = email
        self.default = default
        self.creation_timestamp = creation_timestamp
        self.nb_alias = nb_alias
        self.verified = verified

    def __str__(self) -> str:
        return self.email


class Activity(Object):
    """A SimpleLogin alias activity"""

    def __init__(
        self,
        *,
        id: int | None = None,
        action: str | None = None,
        timestamp: int | None = None,
        from_: str | None = None,
        to_: str | None = None,
        reverse_alias: str | None = None,
        reverse_alias_address: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor

        See SimpleLogin documentation for an explanation of the
        possible fields.
        """
        super().__init__(id=id)
        self.action = action
        self.timestamp = timestamp
        self.from_ = from_ or kwargs.get("from")
        self.to_ = to_ or kwargs.get("to")
        self.reverse_alias = reverse_alias
        self.reverse_alias_address = reverse_alias_address

    def __str__(self) -> str:
        return self.action


class Contact(Object):
    """A SimpleLogin alias contact"""

    def __init__(
        self,
        *,
        id: int | None = None,
        name: str | None = None,
        contact: str | None = None,
        creation_timestamp: int | None = None,
        last_email_sent_timestamp: int | None = None,
        reverse_alias: str | None = None,
        reverse_alias_address: str | None = None,
        block_forward: bool | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor

        See SimpleLogin documentation for an explanation of the
        possible fields.
        """
        super().__init__(id=id)
        self.name = name
        self.contact = contact
        self.creation_timestamp = creation_timestamp
        self.last_email_sent_timestamp = last_email_sent_timestamp
        self.reverse_alias = reverse_alias
        self.reverse_alias_address = reverse_alias_address
        self.block_forward = block_forward

    def __str__(self) -> str:
        return self.contact


class LatestActivity(Object):
    """A SimpleLogin aliases's latest activity"""

    def __init__(
        self,
        *,
        action: str,
        contact: dict,
        timestamp: int,
    ) -> None:
        """
        Constructor

        See SimpleLogin documentation for an explanation of the
        possible fields.
        """
        self.action = action
        self.contact = Contact(
            name=contact.get("name"),
            contact=contact.get("email"),
            reverse_alias=contact.get("reverse_alias"),
        )
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"{self.action} {self.contact.contact}"


class Alias(Object):
    """A SimpleLogin alias"""

    def __init__(
        self,
        *,
        id: int | None = None,
        name: str | None = None,
        email: str | None = None,
        enabled: bool | None = None,
        creation_timestamp: int | None = None,
        note: str | None = None,
        nb_block: int | None = None,
        nb_forward: int | None = None,
        nb_reply: int | None = None,
        support_pgp: bool | None = None,
        disable_pgp: bool | None = None,
        mailboxes: list[Mailbox | dict] | None = None,
        latest_activity: LatestActivity | dict | None = None,
        pinned: bool | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor

        See SimpleLogin documentation for an explanation of the
        possible fields.
        """
        super().__init__(id=id)
        self.name = name
        self.email = email
        self.enabled = enabled
        self.creation_timestamp = creation_timestamp
        self.note = note
        self.nb_block = nb_block
        self.nb_forward = nb_forward
        self.nb_reply = nb_reply
        self.support_pgp = support_pgp
        self.disable_pgp = disable_pgp
        self.pinned = pinned
        if isinstance(latest_activity, dict):
            latest_activity = LatestActivity(**latest_activity)
        self.latest_activity = latest_activity
        self.mailboxes = []
        if mailboxes is None:
            mailboxes = []
        for mailbox in mailboxes:
            box = mailbox
            if not isinstance(box, Mailbox):
                box = Mailbox(**box)
            self.mailboxes.append(box)

    def __str__(self) -> str:
        return self.email
