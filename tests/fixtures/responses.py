import pytest
from responses import Response


@pytest.fixture
def resp_login_no_mfa_success(url_login, sl_login_no_mfa_success):
    return Response(
        method="POST",
        url=url_login,
        status=200,
        json=sl_login_no_mfa_success,
    )


@pytest.fixture
def resp_login_success(url_login, sl_login_success):
    return Response(
        method="POST",
        url=url_login,
        status=200,
        json=sl_login_success,
    )


@pytest.fixture
def resp_login_failure(url_login, sl_login_failure):
    return Response(
        method="POST",
        url=url_login,
        status=400,
        json=sl_login_failure,
    )


@pytest.fixture
def resp_mfa_success(url_mfa, sl_mfa_success):
    return Response(
        method="POST",
        url=url_mfa,
        status=200,
        json=sl_mfa_success,
    )


@pytest.fixture
def resp_mfa_invalid_key(url_mfa, sl_mfa_invalid_key):
    return Response(
        method="POST",
        url=url_mfa,
        status=400,
        json=sl_mfa_invalid_key,
    )


@pytest.fixture
def resp_mfa_invalid_otp(url_mfa, sl_mfa_invalid_otp):
    return Response(
        method="POST",
        url=url_mfa,
        status=400,
        json=sl_mfa_invalid_otp,
    )


@pytest.fixture
def resp_logout_success(url_logout, sl_logout_success):
    return Response(
        method="GET",
        url=url_logout,
        status=200,
        json=sl_logout_success,
    )


@pytest.fixture
def resp_logout_failure(url_logout, sl_logout_failure):
    return Response(
        method="GET",
        url=url_logout,
        status=401,
        json=sl_logout_failure,
    )


@pytest.fixture
def resp_mailbox_list(url_mailboxes, sl_mailbox_list):
    return Response(
        method="GET",
        url=url_mailboxes,
        status=200,
        json=sl_mailbox_list,
    )


@pytest.fixture
def resp_mailbox_create_success(url_mailboxes, sl_mailbox_a):
    return Response(
        method="POST",
        url=url_mailboxes,
        status=201,
        json=sl_mailbox_a,
    )


@pytest.fixture
def resp_mailbox_create_already_exists(url_mailboxes, sl_mailbox_create_already_exists):
    return Response(
        method="POST",
        url=url_mailboxes,
        status=400,
        json=sl_mailbox_create_already_exists,
    )


@pytest.fixture
def resp_mailbox_delete_success(url_mailboxes):
    return Response(
        method="DELETE",
        url=url_mailboxes,
        status=200,
        json={},
    )


@pytest.fixture
def resp_mailbox_delete_failure(url_mailboxes):
    return Response(
        method="DELETE",
        url=url_mailboxes,
        status=400,
        json={},
    )


@pytest.fixture
def resp_mailbox_update_success(url_mailboxes):
    return Response(
        method="PUT",
        url=url_mailboxes,
        status=200,
        json={},
    )


@pytest.fixture
def resp_mailbox_update_failure(url_mailboxes):
    return Response(
        method="PUT",
        url=url_mailboxes,
        status=400,
        json={},
    )


@pytest.fixture
def resp_alias_list(url_aliases, sl_alias_list):
    return Response(
        method="GET",
        url=url_aliases,
        status=200,
        json=sl_alias_list,
    )


@pytest.fixture
def resp_alias_success(url_alias, sl_alias_a):
    return Response(
        method="GET",
        url=url_alias.format(alias_id=sl_alias_a["id"]),
        status=200,
        json=sl_alias_a,
    )


@pytest.fixture
def resp_alias_failure(url_alias, sl_alias_unknown):
    return Response(
        method="GET",
        url=url_alias.format(alias_id=1234),
        status=400,
        json=sl_alias_unknown,
    )


@pytest.fixture
def resp_alias_options(url_alias_options, sl_alias_options):
    return Response(
        method="GET",
        url=url_alias_options,
        status=200,
        json=sl_alias_options,
    )


@pytest.fixture
def resp_alias_custom_success(url_alias_custom, sl_alias_a):
    return Response(
        method="POST",
        url=url_alias_custom,
        status=201,
        json=sl_alias_a,
    )


@pytest.fixture
def resp_alias_random_success(url_alias_random, sl_alias_a):
    return Response(
        method="POST",
        url=url_alias_random,
        status=201,
        json=sl_alias_a,
    )


@pytest.fixture
def resp_alias_delete_success(url_alias, sl_alias_a, sl_alias_delete_success):
    return Response(
        method="DELETE",
        url=url_alias.format(alias_id=sl_alias_a["id"]),
        status=200,
        json=sl_alias_delete_success,
    )


@pytest.fixture
def resp_alias_delete_failure(url_alias, sl_alias_a, sl_alias_delete_failure):
    return Response(
        method="DELETE",
        url=url_alias.format(alias_id=sl_alias_a["id"]),
        status=403,
        json=sl_alias_delete_failure,
    )


@pytest.fixture
def resp_alias_enabled(url_alias_toggle, sl_alias_a, sl_alias_enabled):
    return Response(
        method="POST",
        url=url_alias_toggle.format(alias_id=sl_alias_a["id"]),
        status=200,
        json=sl_alias_enabled,
    )


@pytest.fixture
def resp_alias_toggle_denial(url_alias_toggle, sl_alias_toggle_denial):
    return Response(
        method="POST",
        url=url_alias_toggle.format(alias_id=1234),
        status=403,
        json=sl_alias_toggle_denial,
    )


@pytest.fixture
def resp_alias_activities_list(url_alias_activities, sl_alias_a, sl_activities_list):
    return Response(
        method="GET",
        url=url_alias_activities.format(alias_id=sl_alias_a["id"]),
        status=200,
        json=sl_activities_list,
    )


@pytest.fixture
def resp_alias_update_success(url_alias, sl_alias_a):
    return Response(
        method="PATCH",
        url=url_alias.format(alias_id=sl_alias_a["id"]),
        status=200,
        json={},
    )


@pytest.fixture
def resp_alias_update_failure(url_alias, sl_alias_a, sl_alias_update_failure):
    return Response(
        method="PATCH",
        url=url_alias.format(alias_id=sl_alias_a["id"]),
        status=403,
        json=sl_alias_update_failure,
    )


@pytest.fixture
def resp_alias_contacts_list(url_alias_contacts, sl_alias_a, sl_contacts_list):
    return Response(
        method="GET",
        url=url_alias_contacts.format(alias_id=sl_alias_a["id"]),
        status=200,
        json=sl_contacts_list,
    )


@pytest.fixture
def resp_contact_create_success(url_alias_contacts, sl_alias_a, sl_contact_a):
    return Response(
        method="POST",
        url=url_alias_contacts.format(alias_id=sl_alias_a["id"]),
        status=201,
        json=sl_contact_a,
    )


@pytest.fixture
def resp_contact_create_already_exists(url_alias_contacts, sl_alias_a, sl_contact_a):
    return Response(
        method="POST",
        url=url_alias_contacts.format(alias_id=sl_alias_a["id"]),
        status=200,
        json=sl_contact_a,
    )


@pytest.fixture
def resp_contact_create_unable(
    url_alias_contacts, sl_alias_a, sl_create_contact_unable
):
    return Response(
        method="POST",
        url=url_alias_contacts.format(alias_id=sl_alias_a["id"]),
        status=403,
        json=sl_create_contact_unable,
    )
