from rest_framework import serializers

from commons.serializers import MainModelSerializer, MainPolymorphicSerializer
from commons.serializers.utils import remove_serializer_fields
from files.validators import media_content_type_validator
from users.validators import OwnedByCurrentUser
from schedules.serializers import ScheduleSerializer
from activities.models import Activity, OneTimeActivity, RecurringActivity
from venues.serializers import VenueSerializer
from layouts.serializers import LayoutSerializer


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
            "layout",
        )
        fk_serializers = ActivitySerializer.Meta.fk_serializers | {
            "layout": {"serializer": LayoutSerializer}
        }

    def validate(self, data):
        venue = data.get("venue") or self.get_current("venue")
        layout = data.get("layout") or self.get_current("layout")
        if venue != layout.venue:
            raise serializers.ValidationError(
                {"layout": "The object is not related to the current venue."}
            )
        return super().validate(data)

    def to_representation(self, instance):
        self.fields["layout"].context["activity"] = instance
        return super().to_representation(instance)


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

    def to_representation(self, instance):
        self.fields["schedule"].context["activity"] = instance
        return super().to_representation(instance)

    def get_fields(self):
        from options.serializers import OptionSerializer

        fields = super().get_fields()
        NestedOptionSerializer = remove_serializer_fields(
            OptionSerializer, ["activity"]
        )
        fields["options"] = NestedOptionSerializer(many=True, read_only=True)
        return fields


class PolymorphicActivitySerializer(MainPolymorphicSerializer):
    model_serializer_mapping = {
        OneTimeActivity: OneTimeActivitySerializer,
        RecurringActivity: RecurringActivitySerializer,
    }
    resource_type_field_name = "type"
