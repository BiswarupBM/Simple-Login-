"""
Exceptions raised while processing REST requests
"""


class UnauthenticatedError(ValueError):
    """Raised when an unauthenticated client attempts to access a protected endpoint"""

    pass
