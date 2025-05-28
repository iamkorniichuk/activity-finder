from rest_framework import serializers

from commons.serializers import (
    MainPolymorphicSerializer,
    MainModelSerializer,
    MainWritableNestedModelSerializer,
)
from commons.serializers.utils import remove_serializer_fields
from venues.serializers import VenueSerializer

from .models import VisualObject, Seat, SeatZone, Layout


NestedVenueSerializer = remove_serializer_fields(VenueSerializer, ["layouts"])


class VisualObjectSerializer(MainModelSerializer):
    class Meta:
        model = VisualObject
        fields = ("pk", "name", "position", "size", "rotation")
        read_only_fields = ("pk",)
        extra_kwargs = {
            "position": {"min_value": 0, "max_value": 2560},
            "size": {"min_value": 8, "max_value": 2180},
        }


class SeatSerializer(VisualObjectSerializer):
    class Meta(VisualObjectSerializer.Meta):
        model = Seat
        fields = VisualObjectSerializer.Meta.fields + ("is_booked",)

    is_booked = serializers.SerializerMethodField()

    def get_is_booked(self, obj):
        activity = self.context.get("activity")
        if not activity:
            return None

        bookings = activity.bookings.filter(OneTimeActivityBooking___seat=obj)
        return bookings.exists()


class SeatZoneSerializer(SeatSerializer):
    class Meta(SeatSerializer.Meta):
        model = SeatZone
        fields = SeatSerializer.Meta.fields + ("seat_amount", "booked_seats")

    booked_seats = serializers.SerializerMethodField()

    def get_is_booked(self, obj):
        activity = self.context.get("activity")
        if not activity:
            return None

        bookings = activity.bookings.filter(OneTimeActivityBooking___seat=obj)
        return bookings.count() >= obj.seat_amount

    def get_booked_seats(self, obj):
        activity = self.context.get("activity")
        if not activity:
            return None

        bookings = activity.bookings.filter(OneTimeActivityBooking___seat=obj)
        return bookings.count()


# Inheriting `ModelSerializer` and providing `Meta` make polymorphic serializer writable when nested.
# See: https://github.com/beda-software/drf-writable-nested/issues/139#issuecomment-1311196450
class PolymorphicVisualObjectSerializer(
    MainPolymorphicSerializer,
    serializers.ModelSerializer,
):
    class Meta:
        model = VisualObject
        fields = "__all__"

    model_serializer_mapping = {
        VisualObject: VisualObjectSerializer,
        Seat: SeatSerializer,
        SeatZone: SeatZoneSerializer,
    }
    resource_type_field_name = "type"

    def _get_serializer_from_model_or_instance(self, model_or_instance):
        serializer = super()._get_serializer_from_model_or_instance(model_or_instance)
        serializer.context["activity"] = self.context.get("activity")
        return serializer


class LayoutSerializer(MainWritableNestedModelSerializer):
    class Meta:
        model = Layout
        fields = (
            "pk",
            "name",
            "size",
            "created_by",
            "visual_objects",
            "venue",
        )
        current_user_field = "created_by"
        extra_kwargs = {"size": {"min_value": 180, "max_value": 2560}}

        fk_serializers = {"venue": {"serializer": NestedVenueSerializer}}

    visual_objects = PolymorphicVisualObjectSerializer(many=True)

    def to_representation(self, instance):
        self.fields["visual_objects"].context["activity"] = self.context.get("activity")
        return super().to_representation(instance)
