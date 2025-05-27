from rest_framework import serializers

from commons.serializers import MainModelSerializer, MainPolymorphicSerializer
from commons.serializers.utils import remove_serializer_fields
from files.validators import media_content_type_validator
from users.validators import OwnedByCurrentUser
from schedules.serializers import ScheduleSerializer
from activities.models import Activity, OneTimeActivity, RecurringActivity
from venues.serializers import VenueSerializer


NestedScheduleSerializer = remove_serializer_fields(ScheduleSerializer, ["activities"])
NestedVenueSerializer = remove_serializer_fields(VenueSerializer, ["activities"])


class ActivitySerializer(MainModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "pk",
            "name",
            "description",
            "venue",
            "media",
            "is_published",
        )
        read_only_fields = ("pk", "is_published")
        current_user_field = "created_by"
        multiple_file_fields = {"media": {"validators": [media_content_type_validator]}}
        fk_serializers = {"venue": {"serializer": NestedVenueSerializer}}

    def validate_venue(self, venue):
        if not venue.is_published:
            raise serializers.ValidationError(
                {"venue_pk": "The object is not published."}
            )


class OneTimeActivitySerializer(ActivitySerializer):
    class Meta(ActivitySerializer.Meta):
        model = OneTimeActivity
        fields = ActivitySerializer.Meta.fields + (
            "time_range",
            "date",
        )


class RecurringActivitySerializer(ActivitySerializer):
    class Meta(ActivitySerializer.Meta):
        model = RecurringActivity
        fields = ActivitySerializer.Meta.fields + (
            "schedule",
            "duration",
            "options",
        )
        fk_serializers = {
            "schedule": {
                "serializer": NestedScheduleSerializer,
                "validators": [OwnedByCurrentUser("created_by")],
            }
        }

    def get_fields(self):
        from options.serializers import OptionSerializer

        fields = super().get_fields()
        NestedOptionSerializer = remove_serializer_fields(
            OptionSerializer, ["activity"]
        )
        fields["options"] = NestedOptionSerializer(many=True, read_only=True)
        fields["schedule"].context["activity"] = self.instance
        return fields


class PolymorphicActivitySerializer(MainPolymorphicSerializer):
    model_serializer_mapping = {
        OneTimeActivity: OneTimeActivitySerializer,
        RecurringActivity: RecurringActivitySerializer,
    }
    resource_type_field_name = "type"
