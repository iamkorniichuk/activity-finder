from commons.serializers import MainModelSerializer
from files.validators import media_content_type_validator

from .models import Venue


class VenueSerializer(MainModelSerializer):
    class Meta:
        model = Venue
        fields = (
            "pk",
            "name",
            "description",
            "route",
            "location",
            "created_by",
            "created_at",
            "media",
            "layouts",
            "activities",
            "is_published",
        )
        read_only_fields = ("pk", "created_at", "is_published")
        current_user_field = "created_by"
        multiple_file_fields = {
            "media": {"validators": [media_content_type_validator]},
            "route": {"validators": [media_content_type_validator]},
        }

    def get_fields(self):
        from activities.serializers import PolymorphicActivitySerializer
        from layouts.serializers import LayoutSerializer

        fields = super().get_fields()
        fields["layouts"] = LayoutSerializer(many=True, read_only=True)
        fields["activities"] = PolymorphicActivitySerializer(
            many=True,
            read_only=True,
        )
        return fields
