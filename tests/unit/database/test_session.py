import pytest
from sqlalchemy.exc import IntegrityError

from simplelogincmd.database.models import (
    Mailbox,
)


@pytest.fixture
def new_mailbox(complex_mailbox):
    mb = Mailbox(
        id=complex_mailbox.id + 1,
        email=f"new_{complex_mailbox.email}",
        nb_alias=10,
        verified=False,
        default=False,
        creation_timestamp=789,
    )
    return mb


@pytest.mark.usefixtures("populated_db")
class TestUpsert:

    def test_new_object_is_added_to_session(self, db_access, new_mailbox):
        obj = db_access.session.upsert(new_mailbox)
        assert obj in db_access.session

    def test_merged_object_is_not_added_to_session(self, db_access, new_mailbox):
        assert new_mailbox not in db_access.session
        obj = db_access.session.upsert(new_mailbox)
        assert new_mailbox not in db_access.session

    def test_new_object_persists_in_db(self, db_access, new_mailbox):
        new = db_access.session.upsert(new_mailbox)
        db_access.session.commit()
        selected = db_access.session.get(Mailbox, new.id)
        assert selected is not None
        assert selected is new

    def test_object_with_existing_pk_is_loaded(self, db_access, mailbox):
        # Create a new object based on the old so we're not simply
        # retrieving that same object.
        mb = Mailbox(
            id=mailbox.id,
            email=mailbox.email,
            nb_alias=mailbox.nb_alias,
            verified=mailbox.verified,
            default=mailbox.default,
            creation_timestamp=mailbox.creation_timestamp,
        )
        obj = db_access.session.upsert(mb)
        db_access.session.commit()
        assert obj is mailbox

    def test_modified_object_with_existing_pk_modifies_db(self, db_access, mailbox):
        old_email = mailbox.email
        # Create a new object based on the old so we're not simply
        # retrieving that same object.
        mb = Mailbox(
            id=mailbox.id,
            email=f"updated_{mailbox.email}",
            nb_alias=mailbox.nb_alias,
            verified=mailbox.verified,
            default=mailbox.default,
            creation_timestamp=mailbox.creation_timestamp,
        )
        obj = db_access.session.upsert(mb)
        db_access.session.commit()
        assert obj is mailbox
        assert mailbox.email.startswith("updated_")
        assert mailbox.email != old_email

    def test_new_object_without_pk_creates_new_db_row(self, db_access):
        mb = Mailbox(
            email="random@e.mail",
            nb_alias=42,
            verified=False,
            default=False,
            creation_timestamp=123456,
        )
        obj = db_access.session.upsert(mb)
        db_access.session.commit()
        assert obj.id is not None

    def test_modifications_to_existing_object_persist_in_db(self, db_access, mailbox):
        old_email = mailbox.email
        mailbox.email = f"modified_{mailbox.email}"
        obj = db_access.session.upsert(mailbox)
        db_access.session.commit()
        selected = db_access.session.get(Mailbox, mailbox.id)
        assert selected is mailbox
        assert selected.email.startswith("modified_")
        assert selected.email != old_email

    def test_unique_constraints_on_new_objects_are_respected(
        self, db_access, new_mailbox, mailbox
    ):
        new_mailbox.email = mailbox.email
        obj = db_access.session.upsert(new_mailbox)
        with pytest.raises(IntegrityError):
            db_access.session.commit()

    def test_unique_constraints_on_modified_existing_objects_are_respected(
        self, db_access, new_mailbox, mailbox
    ):
        new_mailbox.id = None
        new_mailbox.email = mailbox.email
        obj = db_access.session.upsert(new_mailbox)
        with pytest.raises(IntegrityError):
            db_access.session.commit()
