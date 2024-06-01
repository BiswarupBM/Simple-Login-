import pytest
import responses

from simplelogincmd.database.models import (
    Activity,
    Alias,
    Contact,
    Mailbox,
)
from simplelogincmd.rest.exceptions import UnauthenticatedError


class TestAccountEndpoints:

    @responses.activate
    def test_login_succeeds_immediately_with_valid_credentials_and_mfa_disabled(
        self, sl_unauthenticated, email, password, api_key, resp_login_no_mfa_success
    ):
        responses.add(resp_login_no_mfa_success)
        success, msg = sl_unauthenticated.login(email, password)
        assert success is True
        assert msg is None
        assert sl_unauthenticated.is_authenticated() is True
        assert sl_unauthenticated.is_mfa_waiting() is False
        assert sl_unauthenticated.api_key == api_key

    @responses.activate
    def test_login_with_valid_credentials_and_mfa_enabled_produces_mfa_key(
        self, sl_unauthenticated, email, password, mfa_key, resp_login_success
    ):
        responses.add(resp_login_success)
        success, msg = sl_unauthenticated.login(email, password)
        assert success is True
        assert msg is None
        assert sl_unauthenticated.is_authenticated() is False
        assert sl_unauthenticated.is_mfa_waiting() is True
        assert sl_unauthenticated.mfa_key == mfa_key

    @responses.activate
    def test_login_with_invalid_credentials_fails(
        self, sl_unauthenticated, email, password, resp_login_failure
    ):
        responses.add(resp_login_failure)
        success, msg = sl_unauthenticated.login(email, password)
        assert success is False
        assert "incorrect" in msg
        assert sl_unauthenticated.is_authenticated() is False
        assert sl_unauthenticated.is_mfa_waiting() is False

    @responses.activate
    def test_mfa_with_valid_credentials_logs_in(
        self, sl_unauthenticated, mfa_token, mfa_key, api_key, resp_mfa_success
    ):
        responses.add(resp_mfa_success)
        success, msg = sl_unauthenticated.mfa(mfa_token, mfa_key)
        assert success is True
        assert msg is None
        assert sl_unauthenticated.is_authenticated() is True
        assert sl_unauthenticated.is_mfa_waiting() is False
        assert sl_unauthenticated.api_key == api_key

    @responses.activate
    def test_mfa_fails_with_invalid_key(
        self, sl_unauthenticated, mfa_token, mfa_key, resp_mfa_invalid_key
    ):
        responses.add(resp_mfa_invalid_key)
        success, msg = sl_unauthenticated.mfa(mfa_token, mfa_key)
        assert success is False
        assert "Invalid" in msg
        assert sl_unauthenticated.is_authenticated() is False

    @responses.activate
    def test_mfa_fails_with_invalid_otp(
        self, sl_unauthenticated, mfa_token, mfa_key, resp_mfa_invalid_otp
    ):
        responses.add(resp_mfa_invalid_otp)
        success, msg = sl_unauthenticated.mfa(mfa_token, mfa_key)
        assert success is False
        assert "OTP" in msg
        assert sl_unauthenticated.is_authenticated() is False

    @responses.activate
    def test_logout_succeeds_when_logged_in(self, sl, api_key, resp_logout_success):
        responses.add(resp_logout_success)
        success = sl.logout()
        assert success is True
        assert sl.is_authenticated() is False

    @responses.activate
    def test_logout_fails_when_not_logged_in(
        self, sl_unauthenticated, resp_logout_failure
    ):
        responses.add(resp_logout_failure)
        with pytest.raises(UnauthenticatedError):
            sl_unauthenticated.logout()


class TestMailboxEndpoints:

    @responses.activate
    def test_returns_mailboxes(self, sl, sl_mailbox_a, resp_mailbox_list):
        responses.add(resp_mailbox_list)
        mailboxes = sl.get_mailboxes()
        assert len(mailboxes) > 0
        assert mailboxes[0] == Mailbox(**sl_mailbox_a)

    @responses.activate
    def test_successful_creation_produces_mailbox(
        self, sl, email, resp_mailbox_create_success
    ):
        responses.add(resp_mailbox_create_success)
        success, obj = sl.create_mailbox(email)
        assert success is True
        assert isinstance(obj, Mailbox)

    @responses.activate
    def test_creation_failure_produces_error(
        self, sl, email, resp_mailbox_create_already_exists
    ):
        responses.add(resp_mailbox_create_already_exists)
        success, obj = sl.create_mailbox(email)
        assert success is False
        assert "already used" in obj

    @responses.activate
    def test_delete_existing_produces_no_error(
        self, sl, sl_mailbox_a, resp_mailbox_delete_success
    ):
        responses.add(resp_mailbox_delete_success)
        success, msg = sl.delete_mailbox(sl_mailbox_a["id"])
        assert success is True
        assert msg is None

    @responses.activate
    def test_delete_failure_produces_error(
        self, sl, sl_mailbox_a, resp_mailbox_delete_failure
    ):
        responses.add(resp_mailbox_delete_failure)
        success, msg = sl.delete_mailbox(sl_mailbox_a["id"])
        assert success is False
        assert isinstance(msg, str)

    @responses.activate
    def test_update_success_returns_no_error(
        self, sl, email, sl_mailbox_a, resp_mailbox_update_success
    ):
        responses.add(resp_mailbox_update_success)
        success, msg = sl.update_mailbox(sl_mailbox_a["id"], email=email)
        assert success is True
        assert msg is None

    @responses.activate
    def test_update_failure_returns_error(
        self, sl, email, sl_mailbox_a, resp_mailbox_update_failure
    ):
        responses.add(resp_mailbox_update_failure)
        success, msg = sl.update_mailbox(sl_mailbox_a["id"], email=email)
        assert success is False
        assert isinstance(msg, str)


class TestAliasEndpoints:

    @responses.activate
    def test_list_without_filters_returns_all(self, sl, sl_alias_a, resp_alias_list):
        responses.add(resp_alias_list)
        aliases = sl.get_aliases()
        assert len(aliases) > 0
        assert aliases[0] == Alias(**sl_alias_a)

    @responses.activate
    def test_get_valid_id_returns_alias(self, sl, sl_alias_a, resp_alias_success):
        responses.add(resp_alias_success)
        success, obj = sl.get_alias(sl_alias_a["id"])
        assert success is True
        assert obj == Alias(**sl_alias_a)

    @responses.activate
    def test_invalid_id_returns_error(self, sl, sl_alias_a, resp_alias_failure):
        responses.add(resp_alias_failure)
        success, obj = sl.get_alias(alias_id=1234)
        assert success is False
        assert "Unknown" in obj

    @responses.activate
    def test_get_options(self, sl, resp_alias_options):
        responses.add(resp_alias_options)
        success, obj = sl.get_alias_options(hostname="test@example.com")
        assert success is True
        assert isinstance(obj, dict)
        assert len(obj.get("suffixes", list())) > 0

    @responses.activate
    def test_create_custom_with_valid_signiture(
        self, sl, sl_mailbox_a, resp_alias_custom_success
    ):
        responses.add(resp_alias_custom_success)
        success, obj = sl.create_custom_alias(
            alias_prefix="prefix",
            signed_suffix="testsecretsuffix",
            mailbox_ids=[sl_mailbox_a["id"]],
        )
        assert success is True
        assert isinstance(obj, Alias)

    @responses.activate
    def test_random_produces_new_alias(self, sl, resp_alias_random_success):
        responses.add(resp_alias_random_success)
        success, obj = sl.create_random_alias()
        assert success is True
        assert isinstance(obj, Alias)

    @responses.activate
    def test_delete_existing_(self, sl, sl_alias_a, resp_alias_delete_success):
        responses.add(resp_alias_delete_success)
        success, msg = sl.delete_alias(alias_id=sl_alias_a["id"])
        assert success is True
        assert msg is None

    @responses.activate
    def test_delete_invalid_(self, sl, sl_alias_a, resp_alias_delete_failure):
        responses.add(resp_alias_delete_failure)
        success, msg = sl.delete_alias(alias_id=sl_alias_a["id"])
        assert success is False
        assert isinstance(msg, str)

    @responses.activate
    def test_enable_alias(self, sl, sl_alias_a, resp_alias_enabled):
        responses.add(resp_alias_enabled)
        success, enabled = sl.toggle_alias(alias_id=sl_alias_a["id"])
        assert success is True
        assert enabled is True

    @responses.activate
    def test_toggling_invalid_id_fails(self, sl, resp_alias_toggle_denial):
        responses.add(resp_alias_toggle_denial)
        success, enabled = sl.toggle_alias(alias_id=1234)
        assert success is False
        assert "Forbidden" in enabled

    @responses.activate
    def test_activities_produces_list(
        self, sl, sl_alias_a, sl_activity_a, resp_alias_activities_list
    ):
        responses.add(resp_alias_activities_list)
        activities = sl.get_alias_activities(alias_id=sl_alias_a["id"])
        assert len(activities) > 0
        assert activities[0] == Activity(**sl_activity_a)

    @responses.activate
    def test_update_valid_id_is_successful(
        self, sl, sl_alias_a, resp_alias_update_success
    ):
        responses.add(resp_alias_update_success)
        success, msg = sl.update_alias(alias_id=sl_alias_a["id"], pinned=True)
        assert success is True
        assert msg is None

    @responses.activate
    def test_update_invalid_id_returns_error_message(
        self, sl, sl_alias_a, resp_alias_update_failure
    ):
        responses.add(resp_alias_update_failure)
        success, msg = sl.update_alias(alias_id=sl_alias_a["id"], pinned=True)
        assert success is False
        assert isinstance(msg, str)

    @responses.activate
    def test_contacts_list(
        self, sl, sl_alias_a, sl_contact_a, resp_alias_contacts_list
    ):
        responses.add(resp_alias_contacts_list)
        contacts = sl.get_alias_contacts(alias_id=sl_alias_a["id"])
        assert len(contacts) > 0
        assert contacts[0] == Contact(**sl_contact_a)

    @responses.activate
    def test_create_new_contact_with_valid_id(
        self, sl, sl_alias_a, sl_contact_a, resp_contact_create_success
    ):
        responses.add(resp_contact_create_success)
        success, obj = sl.create_contact(
            alias_id=sl_alias_a["id"], contact="test@example.com"
        )
        assert success is True
        assert isinstance(obj, Contact)

    @responses.activate
    def test_create_already_existing_contact_succeeds_silently(
        self, sl, sl_alias_a, sl_contact_a, resp_contact_create_already_exists
    ):
        responses.add(resp_contact_create_already_exists)
        success, obj = sl.create_contact(
            alias_id=sl_alias_a["id"], contact="test@example.com"
        )
        assert success is True
        assert isinstance(obj, Contact)

    @responses.activate
    def test_create_contact_without_necessary_permissions(
        self, sl, sl_alias_a, resp_contact_create_unable
    ):
        responses.add(resp_contact_create_unable)
        success, obj = sl.create_contact(
            alias_id=sl_alias_a["id"], contact="test@example.com"
        )
        assert success is False
        assert "Please upgrade" in obj
