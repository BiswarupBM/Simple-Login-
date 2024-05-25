"""
REST-related constants
"""

from types import SimpleNamespace as NS


BASE_URL = "https://api.simplelogin.io"
DEVICE = "SimpleLogin CLI"

# Max number of items the API returns in a single page.
MAX_MODELS_PER_PAGE = 20


ENDPOINT = NS(
    LOGIN="/api/auth/login",
    MFA="/api/auth/mfa",
    LOGOUT="/api/logout",
    MAILBOXES="/api/mailboxes",
    ALIAS_OPTIONS="/api/v5/alias/options",
    ALIAS_CUSTOM="/api/v3/alias/custom/new",
    ALIAS_RANDOM="/api/alias/random/new",
    ALIASES="/api/v2/aliases",
    ALIAS="/api/aliases/{alias_id}",
    ALIAS_TOGGLE="/api/aliases/{alias_id}/toggle",
    ALIAS_ACTIVITIES="/api/aliases/{alias_id}/activities",
    ALIAS_CONTACTS="/api/aliases/{alias_id}/contacts",
)


ALIAS_FILTERS = (
    "pinned",
    "enabled",
    "disabled",
)
