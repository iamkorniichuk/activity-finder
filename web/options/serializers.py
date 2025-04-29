from commons.serializers import MainModelSerializer
from users.validators import OwnedByCurrentUser
from activities.serializers import PolymorphicActivitySerializer

from .models import Option


class OptionSerializer(MainModelSerializer):
    class Meta:
        model = Option
        fields = ("pk", "name", "description", "created_by", "activity")
        read_only_fields = ("pk",)
        current_user_field = "created_by"
        fk_serializers = {
            "activity": {
                "serializer": PolymorphicActivitySerializer,
                "validators": [OwnedByCurrentUser("created_by")],
            }
        }
