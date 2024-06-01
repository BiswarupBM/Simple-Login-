"""
Augmented SQLAlchemy database session
"""

from sqlalchemy.orm import Session

from simplelogincmd.database.models import Object


class SimpleLoginSession(Session):
    """
    An extended database session
    """

    def upsert(self, obj: Object) -> Object:
        """
        Approximate insert-or-update functionality

        If the given object is not in the session, it is merged in,
        loading and updating the object that shares its type and
        primary key if any, or creating a completely new object if one
        of its type with its primary key did not already exist. Objects
        passed in that were already in the session are not touched,, as
        modifications to those objects will be persisted on next commit
        regardless.

        :param obj: The model object to be added/updated
        :type obj: Object

        :return: The created/modified object. Note that in the event of
            a merge, this is *not* the same object that was passed in.
        :rtype: Object
        """
        return obj if obj in self else self.merge(obj)
