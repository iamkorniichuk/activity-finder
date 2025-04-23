from commons.serializers import MainModelSerializer
from activities.serializers import PolymorphicActivitySerializer

from .models import Reaction


class ReactionSerializer(MainModelSerializer):
    class Meta:
        model = Reaction
        fields = (
            "pk",
            "activity",
            "created_by",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"
        fk_serializers = {"activity": PolymorphicActivitySerializer}
        choice_fields = ("type",)
