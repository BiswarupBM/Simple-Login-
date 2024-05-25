import pytest


_obj_id = 0


def _id():
    global _obj_id
    _obj_id += 1
    return _obj_id


@pytest.fixture
def sl_login_no_mfa_success(username, email, api_key):
    return dict(
        name=username,
        email=email,
        mfa_enabled=False,
        mfa_key=None,
        api_key=api_key,
    )


@pytest.fixture
def sl_login_success(username, email, mfa_key):
    return dict(
        name=username,
        email=email,
        mfa_enabled=True,
        mfa_key=mfa_key,
        api_key=None,
    )


@pytest.fixture
def sl_login_failure():
    return dict(
        error="Email or password incorrect",
    )


@pytest.fixture
def sl_mfa_success(username, email, api_key):
    return dict(
        name=username,
        email=email,
        api_key=api_key,
    )


@pytest.fixture
def sl_mfa_invalid_key():
    return dict(
        error="Invalid mfa_key",
    )


@pytest.fixture
def sl_mfa_invalid_otp():
    return dict(
        error="Wrong TOTP Token",
    )


@pytest.fixture
def sl_logout_success():
    return dict(
        msg="User is logged out",
    )


@pytest.fixture
def sl_logout_failure():
    return dict(
        error="Wrong api key",
    )


@pytest.fixture
def sl_mailbox_a():
    return dict(
        id=_id(),
        email="a@b.c",
        default=True,
        creation_timestamp=1590918512,
        nb_alias=10,
        verified=True,
    )


@pytest.fixture
def sl_mailbox_b():
    return dict(
        id=_id(),
        email="m1@example.com",
        default=False,
        creation_timestamp=1590918512,
        nb_alias=0,
        verified=False,
    )


@pytest.fixture
def sl_mailbox_list(sl_mailbox_a, sl_mailbox_b):
    return dict(
        mailboxes=[
            sl_mailbox_a,
            sl_mailbox_b,
        ],
    )


@pytest.fixture
def sl_mailbox_create_already_exists(email):
    return dict(
        error=f"{email} already used",
    )


@pytest.fixture
def sl_alias_a(username, email, sl_mailbox_a):
    return dict(
        id=_id(),
        name=username,
        email=email,
        enabled=False,
        creation_timestamp=1234567890,
        note="Some notes",
        nb_block=1,
        nb_forward=12,
        nb_reply=0,
        support_pgp=True,
        disable_pgp=False,
        mailboxes=[
            sl_mailbox_a,
        ],
        latest_activity=dict(
            action="forward",
            timestamp=1029384756,
            contact=dict(
                name=username,
                email=email,
                reverse_alias="reversed@alias.com",
            ),
        ),
    )


@pytest.fixture
def sl_alias_b(sl_mailbox_b):
    return dict(
        id=_id(),
        name="Some Name",
        email="prefix1.cat@sl.local",
        creation_timestamp=1586195834,
        enabled=True,
        note=None,
        nb_block=0,
        nb_forward=1,
        nb_reply=0,
        pinned=True,
        mailboxes=[
            sl_mailbox_b,
        ],
        latest_activity=dict(
            action="forward",
            timestamp=4,
            contact=dict(
                name=None,
                email="c1@example.com",
                reverse_aliase='"c1@example.com" <re1@SL>',
            ),
        ),
    )


@pytest.fixture
def sl_alias_list(sl_alias_a, sl_alias_b):
    return dict(
        aliases=[
            sl_alias_a,
            sl_alias_b,
        ],
    )


@pytest.fixture
def sl_alias_unknown():
    return dict(
        error="Unknown error",
    )


@pytest.fixture
def sl_alias_options():
    return dict(
        can_create=True,
        prefix_suggestion="test",
        suffixes=[
            dict(
                signed_suffix=".cat@d1.test.X6_7OQ.0e9NbZHE_bQvuAapT6NdBml9m6Q",
                suffix=".cat@d1.test",
                is_custom=True,
                is_premium=False,
            ),
            dict(
                signed_suffix=".chat@d2.test.X6_7OQ.TTgCrfqPj7UmlY723YsDTHhkess",
                suffix=".chat@d2.test",
                is_custom=False,
                is_premium=False,
            ),
            dict(
                signed_suffix=".yeah@sl.local.X6_7OQ.i8XL4xsMsn7dxDEWU8eF-Zap0qo",
                suffix=".yeah@sl.local",
                is_custom=True,
                is_premium=False,
            ),
        ],
    )


@pytest.fixture
def sl_alias_delete_success():
    return dict(
        deleted=True,
    )


@pytest.fixture
def sl_alias_delete_failure():
    return dict(
        error="Forbidden",
    )


@pytest.fixture
def sl_alias_enabled():
    return dict(
        enabled=True,
    )


@pytest.fixture
def sl_alias_disabled():
    return dict(
        enabled=False,
    )


@pytest.fixture
def sl_alias_toggle_denial():
    return dict(
        error="Forbidden",
    )


@pytest.fixture
def sl_activity_a():
    return dict(
        id=None,
        action="reply",
        timestamp=1580903760,
        from_="yes_meo_chat@sl.local",
        to_="marketing@example.com",
        reverse_alias='"marketing at example.com" <reply@a.b>',
        reverse_alias_address="reply@a.b",
    )


@pytest.fixture
def sl_activity_b():
    return dict(
        id=None,
        action="forward",
        timestamp=1234567890,
        from_="test@example.com",
        to_="other@site.net",
        reverse_alias='"other@site.net" <reply@a.c>',
        reverse_alias_address="reply@a.c",
    )


@pytest.fixture
def sl_activities_list(sl_activity_a, sl_activity_b):
    return dict(
        activities=[
            sl_activity_a,
            sl_activity_b,
        ]
    )


@pytest.fixture
def sl_alias_update_failure():
    return dict(
        error="Forbidden",
    )


@pytest.fixture
def sl_contact_a():
    return dict(
        id=_id(),
        contact="marketing@example.com",
        creation_timestamp=1582284900,
        last_email_sent_timestamp=None,
        reverse_alias="marketing at example.com <reply+bzvpazcdedcgcpztehxzgjgzmxskqa@sl.co>",
        block_forward=False,
    )


@pytest.fixture
def sl_contact_b():
    return dict(
        id=_id(),
        contact="newsletter@example.com",
        creation_timestamp=1582284900,
        last_email_sent_timestamp=1582284900,
        reverse_alias="newsletter at example.com <reply+bzvpazcdedcgcpztehxzgjgzmxskqa@sl.co>",
        reverse_alias_address="reply+bzvpazcdedcgcpztehxzgjgzmxskqa@sl.co",
        block_forward=True,
    )


@pytest.fixture
def sl_contacts_list(sl_contact_a, sl_contact_b):
    return dict(
        contacts=[
            sl_contact_a,
            sl_contact_b,
        ],
    )


@pytest.fixture
def sl_create_contact_unable():
    return dict(
        error="Please upgrade to create a reverse-alias",
    )
