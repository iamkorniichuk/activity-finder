from rest_framework import serializers


class OwnedByCurrentUser:
    requires_context = True
    message = "Object is not owned by current user."

    def __init__(self, user_field):
        self.user_field = user_field

    def __call__(self, obj, serializer_field):
        current_user = serializer_field.context["request"].user
        obj_user = getattr(obj, self.user_field)
        if obj_user != current_user:
            raise serializers.ValidationError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, OwnedByCurrentUser)
            and self.user_field == other.user_field
        )
