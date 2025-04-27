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
        )
        read_only_fields = ("pk", "created_at")
        current_user_field = "created_by"
        multiple_file_fields = {
            "media": {"validators": [media_content_type_validator]},
            "route": {"validators": [media_content_type_validator]},
        }
