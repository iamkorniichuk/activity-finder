from rest_framework.permissions import BasePermission, SAFE_METHODS
from collections.abc import Iterable

from commons.utils import resolve_nested_attribute


class OwnedByCurrentUser(BasePermission):
    """
    Checks the ownership if the user is associated with the object.

    Relations support:
        - Direct: `created_by` field of the object matches the current user.
        - Nested relations: `activity.created_by` field in a related model matches the current user.
        - Many: the current user is in a `ManyToMany` or `ForeignKey` field of related users.
        - Itself: the current user matches the object itself.
    """

    error_message = "Object is not owned by current user."

    def __init__(self, field_name=None):
        self.message = {field_name: self.error_message}
        self.field_name = field_name

    def has_object_permission(self, request, view, obj):
        current_user = request.user
        obj = resolve_nested_attribute(obj, self.field_name)

        return self.is_user_related(obj, current_user)

    def is_user_related(self, obj, user):
        if isinstance(obj, Iterable):
            return user in obj
        return obj == user


class OwnedByCurrentUserOrReadOnly(OwnedByCurrentUser):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)
