import pytest

from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


def test_init_accepts_extra_arguments():
    # No asserts necessary. Only testing that __init__ does not raise.
    Alias(extratestkwarg=True)
    Mailbox(extratestkwarg=True)


class TestFieldGetters:

    def test_get_existing_field(self, mailbox):
        assert mailbox.get("id") == 1
        assert mailbox.get("email") == "test@site.com"
        assert mailbox.get("verified") is True

    def test_get_invalid_field_is_none(self, mailbox):
        assert mailbox.get("faketestfield") is None

    def test_field_as_string_returns_strings(self, complex_mailbox):
        assert complex_mailbox.get_string("id") == "2"
        assert complex_mailbox.get_string("email") == "more@tests.io"
        assert complex_mailbox.get_string("verified") == "Y"
        assert complex_mailbox.get_string("default") == "N"
        assert complex_mailbox.get_string("list_attr") == "1, 2, 3"
        assert complex_mailbox.get_string("dict_attr") == str({"key": "value"})

    def test_get_undefined_field_as_string_is_empty_string(self, mailbox):
        assert mailbox.get_string("faketestfield") == ""


@pytest.mark.usefixtures("populated_db")
class TestIdentifiers:

    def test_valid_numeric_id_returns_one(self, db_access):
        results = Mailbox.resolve_identifier(db_access.session, 1)
        assert len(results) == 1

    def test_invalid_numeric_id_returns_zero(self, db_access):
        results = Mailbox.resolve_identifier(db_access.session, 525600)
        assert len(results) == 0

    def test_full_mailbox_email_matches_one(self, db_access):
        results = Mailbox.resolve_identifier(db_access.session, "test@site.com")
        assert len(results) == 1
        assert results[0].id == 1

    def test_partial_mailbox_email_matches_multiple(self, db_access):
        results = Mailbox.resolve_identifier(db_access.session, "test")
        assert len(results) > 1

    def test_invalid_string_identifier_returns_zero(self, db_access):
        results = Mailbox.resolve_identifier(
            db_access.session, "thisstringwontmatchanything"
        )
        assert len(results) == 0

    def test_alias_identifier_matches_email(self, db_access):
        results = Alias.resolve_identifier(db_access.session, "sl.com")
        assert len(results) == 1

    def test_alias_identifier_matches_note(self, db_access):
        results = Alias.resolve_identifier(db_access.session, "test")
        assert len(results) == 1
