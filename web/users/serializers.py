from commons.serializers import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "image",
            "display_name",
            "description",
            "birth_date",
        )
        read_only_fields = ("pk",)
