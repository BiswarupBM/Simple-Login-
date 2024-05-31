"""
Manage requests and responses to the SimpleLogin API
"""

from simplelogincmd.rest import const, util
from simplelogincmd.rest.client import Client
from simplelogincmd.database.models import (
    Activity,
    Alias,
    Contact,
    Mailbox,
)


class SimpleLogin:
    """SimpleLogin client"""

    def __init__(self, client_cls: type = Client) -> None:
        """
        Constructor

        :param client_cls: The type of :class:`simplelogincmd.rest.client.Client`
            to use for handling requests, defaults to :class:`Client`
        :type client_cls: Type
        """
        self.client = client_cls(const.BASE_URL)
        self._api_key = None
        self._mfa_key = None

    def _auth_headers(self) -> dict:
        """
        Get the headers necessary for making requests to the API

        Note that if the client is not authenticated, this will provide
        invalid headers. Use this only in methods decorated with
        :func:`~simplelogincmd.rest.util.require_authentication` to ensure that
        exceptions are raised before a bogus request is made to the API.
        """
        return {"Authentication": self._api_key}

    @property
    def api_key(self) -> str | None:
        """
        The api_key that verifies the user's identity to the API

        :return: The client's API key, or None if the client is not yet
            authenticated. Almost all requests will fail without
            authentication
        :rtype: str | None
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value) -> None:
        self._api_key = value

    @property
    def mfa_key(self) -> str | None:
        """
        The MFA key which SimpleLogin sends to verify an MFA request

        :return: The MFA key if any has been set
        :rtype: str | None
        """
        return self._mfa_key

    def is_authenticated(self) -> bool:
        """
        Whether the client is fully authenticated

        If so, the client is ready to use almost all of SimpleLogin's functionality

        :rtype: bool
        """
        return self.api_key is not None

    def is_mfa_waiting(self) -> bool:
        """
        Whether the client is waiting to be authenticated via MFA

        If so, then the client is unable to make most requests. Note,
        however, that if it is not waiting, it's not necessarily fully
        authenticated--it may not have made any authentication attempt
        at all, or may have failed. Use :meth:`is_authenticated` to
        ensure that the login process has completed fully.

        :rtype: bool
        """
        return self.mfa_key is not None

    def login(
        self,
        email: str,
        password: str,
        device: str | None = None,
    ) -> tuple[bool, str | None]:
        """
        Attempt to log in to SimpleLogin

        Note that even if this returns True, the client might still not
        be fully authenticated. Use :meth:`is_mfa_waiting` and
        :meth:`is_authenticated` to check its state, and :meth:`mfa` to
        attempt MFA if necessary.

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the login was successful, and an optional error
            message suitable for displaying to users
        :rtype: tuple[bool, str | None]
        """
        endpoint = const.ENDPOINT.LOGIN
        body = dict(
            email=email,
            password=password,
            device=device or const.DEVICE,
        )
        success, json = self.client.post(endpoint, json=body)
        if not success:
            return success, json.get("error", "Login failed")
        if (mfa_key := json.get("mfa_key")) is not None:
            self._mfa_key = mfa_key
        elif (api_key := json.get("api_key")) is not None:
            self._api_key = api_key
        return success, None

    def mfa(
        self,
        mfa_token: str,
        mfa_key: str,
        device: str | None = None,
    ) -> tuple[bool, str | None]:
        """
        Attempt to authenticate via MFA

        This should never be used before calling :meth:`login`. If it
        returns true, you can be certain that the client is fully
        authenticated

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether MFA was successful, and an optional error
            message suitable for displaying to the user
        :rtype: tuple[bool, str | None]
        """
        endpoint = const.ENDPOINT.MFA
        body = dict(
            mfa_token=mfa_token,
            mfa_key=mfa_key,
            device=device or const.DEVICE,
        )
        success, json = self.client.post(endpoint, json=body)
        if not success:
            return success, json.get("error", "MFA failed")
        self._api_key = json.get("api_key")
        return success, None

    @util.require_authentication
    def logout(self) -> bool:
        """
        Log out of SimpleLogin

        :return: Whether logout was successful (this is tecnically
            always True, because
            :exc:`~simplelogincmd.rest.exceptions.UnauthenticatedError`
            is raised if the client is not logged in)
        :rtype: bool
        """
        endpoint = const.ENDPOINT.LOGOUT
        success, json = self.client.get(endpoint, headers=self._auth_headers())
        if success:
            self._api_key = None
        return success

    @util.require_authentication
    def get_mailboxes(self) -> list[Mailbox]:
        """
        Get all the user's mailboxes

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of mailboxes
        :rtype: list[Mailbox]
        """
        endpoint = const.ENDPOINT.MAILBOXES
        success, json = self.client.get(endpoint, headers=self._auth_headers())
        info_list = json.get("mailboxes", list())
        mailboxes = [Mailbox(**info) for info in info_list]
        return mailboxes

    @util.require_authentication
    def create_mailbox(self, email: str) -> tuple[bool, Mailbox | str]:
        """
        Create a new mailbox

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether creation succeeded, and either an error message
            or the new mailbox, as appropriate
        :rtype: tuple[bool, Mailbox | str]
        """
        endpoint = const.ENDPOINT.MAILBOXES
        headers = self._auth_headers()
        body = dict(
            email=email,
        )
        success, json = self.client.post(endpoint, json=body, headers=headers)
        if not success:
            return success, json.get("error", "Mailbox creation failed")
        return success, Mailbox(**json)

    @util.require_authentication
    def delete_mailbox(
        self,
        mailbox_id: int,
        transfer_aliases_to: int = -1,
    ) -> tuple[bool, str | None]:
        """
        Delete a mailbox

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the deletion succeeded, and an optional error
            message
        :rtype: tuple[bool, str | None]
        """
        endpoint = const.ENDPOINT.MAILBOXES
        headers = self._auth_headers()
        params = dict(
            mailbox_id=mailbox_id,
        )
        body = dict(
            transfer_aliases_to=transfer_aliases_to,
        )
        success, json = self.client.delete(endpoint, params=params, headers=headers)
        if not success:
            return success, json.get("error", "Mailbox deletion failed")
        return success, None

    @util.require_authentication
    def update_mailbox(
        self,
        mailbox_id: int,
        email: str | None = None,
        default: bool | None = None,
        cancel_email_change: bool | None = None,
    ) -> tuple[bool, str | None]:
        """
        Modify a mailbox's properties

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the update succeeded, and an optional error
            message
        :rtype: tuple[bool, str | None]
        """
        endpoint = const.ENDPOINT.MAILBOXES
        headers = self._auth_headers()
        params = dict(
            mailbox_id=mailbox_id,
        )
        body = {}
        if email is not None:
            body["email"] = email
        if default is not None:
            body["default"] = default
        if cancel_email_change is not None:
            body["cancel_email_change"] = cancel_email_change
        success, json = self.client.put(
            endpoint, params=params, json=body, headers=headers
        )
        if not success:
            return success, json.get("error", "Failed to update mailbox")
        return success, None

    @util.require_authentication
    def get_aliases(self, page_id: int = 0, query: str | None = None) -> list[Alias]:
        """
        Get a page of the user's aliases

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of aliases
        :rtype: list[Alias]
        """
        endpoint = const.ENDPOINT.ALIASES
        headers = self._auth_headers()
        params = dict(
            page_id=page_id,
        )
        body = None
        if query is not None:
            query = query.lower()
            if query in const.ALIAS_FILTERS:
                body = {"query": query}
        success, json = self.client.get(
            endpoint, params=params, json=body, headers=headers
        )
        info_list = json.get("aliases", list())
        aliases = [Alias(**info) for info in info_list]
        return aliases

    @util.require_authentication
    def get_all_aliases(self, query: str | None = None) -> list[Alias]:
        """
        Get a list of all the user's aliases

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of aliases
        :rtype: list[Alias]
        """
        all_aliases = []
        page_id = 0
        while True:
            aliases = self.get_aliases(page_id=page_id, query=query)
            all_aliases.extend(aliases)
            if len(aliases) < const.MAX_MODELS_PER_PAGE:
                break
            page_id += 1
        return all_aliases

    @util.require_authentication
    def get_alias(self, alias_id: int) -> tuple[bool, Alias | str]:
        """
        Get one of a user's aliases

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the operation succeeded, and either the alias
            or an error message, as appropriate
        :rtype: tuple[bool, Alias | str]
        """
        endpoint = const.ENDPOINT.ALIAS.format(alias_id=alias_id)
        headers = self._auth_headers()
        success, json = self.client.get(endpoint, headers=headers)
        if not success:
            return success, json.get("error", f"Failed to get alias {alias_id}")
        return success, Alias(**json)

    @util.require_authentication
    def get_alias_options(self, hostname: str | None = None) -> tuple[bool, dict | str]:
        """
        Get options for a new custom alias

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the operation succeeded, and the alias options
            or an error message, as appropriate. See SimpleLogin's
            documentation for an explanation of the fields returned
        :rtype: tuple[bool, dict | str]
        """
        endpoint = const.ENDPOINT.ALIAS_OPTIONS
        headers = self._auth_headers()
        params = {}
        if hostname is not None:
            params["hostname"] = hostname
        success, json = self.client.get(endpoint, params=params, headers=headers)
        if not success:
            return success, json.get("error", "Failed to get alias options")
        return success, json

    @util.require_authentication
    def create_custom_alias(
        self,
        *,
        alias_prefix: str,
        signed_suffix: str,
        mailbox_ids: list[int],
        note: str | None = None,
        name: str | None = None,
        hostname: str | None = None,
    ) -> tuple[bool, Alias | str]:
        """
        Create a new custom alias

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the creation succeeded, and the new alias or
            an error message, as appropriate
        :rtype: tuple[bool, Alias | str]
        """
        endpoint = const.ENDPOINT.ALIAS_CUSTOM
        headers = self._auth_headers()
        params = None
        if hostname is not None:
            params = {"hostname": hostname}
        body = dict(
            alias_prefix=alias_prefix,
            signed_suffix=signed_suffix,
            mailbox_ids=list(mailbox_ids),
            note=note,
            name=name,
        )
        success, json = self.client.post(
            endpoint, params=params, json=body, headers=headers
        )
        if not success:
            return success, json.get("error", "Failed to create custom alias")
        return success, Alias(**json)

    @util.require_authentication
    def create_random_alias(
        self,
        hostname: str | None = None,
        mode: str | None = None,
        note: str | None = None,
    ) -> tuple[bool, Alias | str]:
        """
        Create a new random alias

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the creation succeeded, and the new alias or
            an error message, as appropriate
        :rtype: tuple[bool, Alias | str]
        """
        endpoint = const.ENDPOINT.ALIAS_RANDOM
        headers = self._auth_headers()
        params = {}
        if hostname is not None:
            params["hostname"] = hostname
        if mode is not None:
            params["mode"] = mode
        body = None
        if note is not None:
            body = {"note": note}
        success, json = self.client.post(
            endpoint, params=params, json=body, headers=headers
        )
        if not success:
            return success, json.get("error", "Failed to create random alias")
        return success, Alias(**json)

    @util.require_authentication
    def delete_alias(self, alias_id: int) -> tuple[bool, str | None]:
        """
        Delete an alias

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the deletion succeeded, and an optional error
            message
        :rtype: tuple[bool, str | None]
        """
        endpoint = const.ENDPOINT.ALIAS.format(alias_id=alias_id)
        headers = self._auth_headers()
        success, json = self.client.delete(endpoint, headers=headers)
        if not success:
            return success, json.get("error", "Failed to delete alias")
        return success, None

    @util.require_authentication
    def toggle_alias(self, alias_id: int) -> tuple[bool, bool | str]:
        """
        Toggle an alias's enabled state

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the toggle succeeded, and the alias's new
            state or an error message, as appropriate
        :rtype: tuple[bool, bool | str]
        """
        endpoint = const.ENDPOINT.ALIAS_TOGGLE.format(alias_id=alias_id)
        headers = self._auth_headers()
        success, json = self.client.post(endpoint, headers=headers)
        if not success:
            return success, json.get("error", "Failed to toggle alias")
        return success, json.get("enabled")

    @util.require_authentication
    def get_alias_activities(self, alias_id: int, page_id: int = 0) -> list[Activity]:
        """
        Get a single page of an alias's activity records

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of activities
        :rtype: list[Activity]
        """
        endpoint = const.ENDPOINT.ALIAS_ACTIVITIES.format(alias_id=alias_id)
        headers = self._auth_headers()
        params = dict(
            page_id=page_id,
        )
        success, json = self.client.get(endpoint, params=params, headers=headers)
        info_list = json.get("activities", list())
        activities = [Activity(**info) for info in info_list]
        return activities

    @util.require_authentication
    def get_all_alias_activities(self, alias_id: int) -> list[Activity]:
        """
        Get all the activity records for the given alias

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of activities
        :rtype: list[Activity]
        """
        all_activities = []
        page_id = 0
        while True:
            activities = self.get_alias_activities(alias_id=alias_id, page_id=page_id)
            all_activities.extend(activities)
            if len(activities) < const.MAX_MODELS_PER_PAGE:
                break
            page_id += 1
        return all_activities

    @util.require_authentication
    def update_alias(
        self,
        *,
        alias_id: int,
        note: str | None = None,
        name: str | None = None,
        mailbox_ids: list[int] | None = None,
        disable_pgp: bool | None = None,
        pinned: bool | None = None,
    ) -> tuple[bool, str | None]:
        """
        Modify an alias's properties

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: Whether the update succeeded, and an optional error
            message
        :rtype: tuple[bool, str | None]
        """
        endpoint = const.ENDPOINT.ALIAS.format(alias_id=alias_id)
        headers = self._auth_headers()
        body = {}
        if note is not None:
            body["note"] = note
        if name is not None:
            body["name"] = name
        if mailbox_ids is not None:
            body["mailbox_ids"] = list(mailbox_ids)
        if disable_pgp is not None:
            body["disable_pgp"] = disable_pgp
        if pinned is not None:
            body["pinned"] = pinned
        success, json = self.client.patch(endpoint, json=body, headers=headers)
        if not success:
            return success, json.get("error", "Failed to update alias")
        return success, None

    @util.require_authentication
    def get_alias_contacts(self, alias_id: int, page_id: int = 0) -> list[Contact]:
        """
        Get a single page of an alias's contacts

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of contacts
        :rtype: list[Contact]
        """
        endpoint = const.ENDPOINT.ALIAS_CONTACTS.format(alias_id=alias_id)
        headers = self._auth_headers()
        params = dict(
            page_id=page_id,
        )
        success, json = self.client.get(endpoint, params=params, headers=headers)
        info_list = json.get("contacts", list())
        contacts = [Contact(**info) for info in info_list]
        return contacts

    @util.require_authentication
    def get_all_alias_contacts(self, alias_id: int) -> list[Contact]:
        """
        Get all of an alias's contacts

        See SimpleLogin's documentation for an explanation of the
        parameters.

        :return: A list, which might be empty, of contacts
        :rtype: list[Contact]
        """
        all_contacts = []
        page_id = 0
        while True:
            contacts = self.get_alias_contacts(alias_id=alias_id, page_id=page_id)
            all_contacts.extend(contacts)
            if len(contacts) < const.MAX_MODELS_PER_PAGE:
                break
            page_id += 1
        return all_contacts

    @util.require_authentication
    def create_contact(self, alias_id: int, contact: str) -> tuple[bool, Contact | str]:
        """
        Create a new contact for the given alias

        See the Simplelogin documentation for an explanation of the
        parameters.

        :return: Whether the creation succeeded, and the new contact
            or an error message, as appropriate
        :rtype: tuple[bool, Contact | str]
        """
        endpoint = const.ENDPOINT.ALIAS_CONTACTS.format(alias_id=alias_id)
        headers = self._auth_headers()
        body = dict(
            contact=contact,
        )
        success, json = self.client.post(endpoint, json=body, headers=headers)
        if not success:
            return success, json.get("error", "Failed to create contact")
        return success, Contact(**json)
