from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from commons.serializers import MainModelSerializer
from files.validators import media_content_type_validator
from users.validators import OwnedByCurrentUser
from schedules.serializers import ScheduleSerializer
from activities.models import Activity, OneTimeActivity, RecurringActivity
from venues.serializers import VenueSerializer


class ActivitySerializer(MainModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "pk",
            "name",
            "description",
            "venue",
            "is_remote",
            "media",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"
        multiple_file_fields = {"media": {"validators": [media_content_type_validator]}}
        fk_serializers = {"venue": {"serializer": VenueSerializer}}

    def validate(self, data):
        venue = self.get_current("venue", data)
        is_remote = self.get_current("is_remote", data)
        if not is_remote and not venue:
            raise serializers.ValidationError(
                {"venue": "Required when `is_remote` is false."}
            )
        return super().validate(data)


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
        )
        fk_serializers = {
            "schedule": {
                "serializer": ScheduleSerializer,
                "validators": [OwnedByCurrentUser("created_by")],
            }
        }


class PolymorphicActivitySerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        OneTimeActivity: OneTimeActivitySerializer,
        RecurringActivity: RecurringActivitySerializer,
    }
    resource_type_field_name = "type"

    def run_validation(self, data):
        if self.instance and self.resource_type_field_name in data:
            new_type = self._get_resource_type_from_mapping(data)
            old_type = self.instance.__class__.__name__
            if new_type != old_type:
                raise serializers.ValidationError(
                    {
                        self.resource_type_field_name: "You can't change `type` on created activity."
                    }
                )
        return super().run_validation(data)
