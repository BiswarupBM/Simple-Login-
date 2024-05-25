"""
REST utilities
"""

from functools import wraps

from simplelogincmd.rest.exceptions import UnauthenticatedError


def require_authentication(f):
    """
    Decorate a method to raise an error if its instance has no API key

    Help to prevent bogus calls to the API by raising
    :exc:`UnauthenticatedError` before any requests are made if the
    instance's
    :meth:`~simplelogincmd.rest.simplelogin.SimpleLogin.is_authenticated`
    method returns False.  Also add a note of this behavior to the
    decorated method's docstring so that it is documented in only one
    place.

    :param f: The method to decorate
    :type f: Callable[[Any], Any]

    :return: The decorated method
    :rtype: Callable[[Any], Any]
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not self.is_authenticated():
            raise UnauthenticatedError()
        return f(self, *args, **kwargs)

    # Add a ":raise:" field to the method's docstring, attempting, within
    # reason, to maintain the docstring's format for Sphinx's sake. This
    # will appear only in interactive sessions and in generated docs,
    # but we do it here so as not to require a note be made in every doc
    # of every decorated method--the presence of the decorator alone
    # should suffice for those looking at the source code.
    doc = wrapper.__doc__
    addition = ":raise UnauthenticatedError: If :obj:`self` is not authenticated"
    if doc is None:
        # `wrapper` has no doc, so simply set it.
        new_doc = addition
    else:
        # Look for the indentation level of the latest line (this will
        # produce incorrect results if a multiline docstring does not
        # end with a newline, but we leave that to the doc-writer in
        # order to keep this somewhat simple.
        indentation = ""
        lines = doc.splitlines()
        for line in reversed(lines):
            if line.isspace():
                indentation = line
                break
        if indentation == "":
            # Doc was probably a one-liner with no indentation. Make it
            # an unindented multi-paragraph doc.
            new_doc = f"\n{doc}\n\n{addition}\n"
        else:
            # Add a new paragraph at the same indentation level as the
            # latest.
            new_doc = f"{doc}\n{indentation}{addition}\n{indentation}"

        wrapper.__doc__ = new_doc

    return wrapper
