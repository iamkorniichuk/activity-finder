from rest_framework import serializers

from commons.serializers import MainModelSerializer, MainPolymorphicSerializer
from options.serializers import OptionSerializer
from layouts.serializers import PolymorphicVisualObjectSerializer
from activities.serializers import PolymorphicActivitySerializer, Activity

from .models import Booking, OneTimeActivityBooking, RecurringActivityBooking


class BookingSerializer(MainModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk",)
        read_only_fields = ("pk",)
        fk_serializers = {
            "activity": {"serializer": PolymorphicActivitySerializer},
        }


class OneTimeActivityBookingSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        model = OneTimeActivityBooking
        fields = BookingSerializer.Meta.fields + (
            "seat",
            "booked_by",
            "booked_at",
        )
        fk_serializers = BookingSerializer.Meta.fk_serializers | {
            "seat": {"serializer": PolymorphicVisualObjectSerializer},
        }
        current_user_field = "booked_by"

    def validate(self, data):
        activity = data.get("activity") or self.get_current("activity")
        seat = data.get("seat") or self.get_current("seat")
        self.validate_is_seat_related_to_activity(seat, activity)
        self.validate_is_seat_free(seat, activity)

        return super().validate(data)

    def validate_is_seat_related_to_activity(self, seat, activity):
        if activity.venue != seat.layout.venue:
            raise serializers.ValidationError(
                {"seat": "The object is not related to the current activity."}
            )

    def validate_is_seat_free(self, seat, activity):
        seat_type = seat.__class__.__name__
        seat_bookings = OneTimeActivityBooking.objects.filter(
            activity=activity, seat=seat
        )
        is_seat_occupied = seat_type == "Seat" and seat_bookings.exists()
        is_seat_zone_occupied = (
            seat_type == "SeatZone" and seat_bookings.count() >= seat.seat_amount
        )
        if is_seat_occupied or is_seat_zone_occupied:
            raise serializers.ValidationError({"seat": "The object is occupied"})


class RecurringActivityBookingSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        model = RecurringActivityBooking
        fields = BookingSerializer.Meta.fields + (
            "week_day",
            "time",
            "booked_by",
            "booked_at",
            "option",
            "note",
        )
        choice_display_fields = ("week_day",)

        current_user_field = "booked_by"
        fk_serializers = BookingSerializer.Meta.fk_serializers | {
            "option": {"serializer": OptionSerializer},
        }

    def validate(self, data):
        activity = data.get("activity") or self.get_current("activity")
        option = data.get("option") or self.get_current("option")
        self.validate_is_option_related_to_activity(option, activity)

        week_day = data.get("week_day") or self.get_current("week_day")
        time = data.get("time") or self.get_current("time")
        schedule = activity.schedule

        self.validate_is_within_schedule(schedule, week_day, time)
        self.validate_is_booking_free(activity, week_day, time)

        return super().validate(data)

    def validate_is_option_related_to_activity(self, option, activity):
        if activity != option.activity:
            raise serializers.ValidationError(
                {"option": "The object is not related to the current activity."}
            )

    def validate_is_within_schedule(self, schedule, week_day, time):
        for obj in schedule.work_days.all():
            day = obj.week_day
            if day == week_day:
                for slot in obj.slots:
                    if slot == time:
                        return

                raise serializers.ValidationError(
                    {"time": "Selected time doesn't suit the schedule"}
                )

        raise serializers.ValidationError(
            {"week_day": "Selected time doesn't suit the schedule"}
        )

    def validate_is_booking_free(self, activity, week_day, time):
        same_booking = RecurringActivityBooking.objects.filter(
            activity=activity,
            week_day=week_day,
            time=time,
        )
        if same_booking.exists():
            raise serializers.ValidationError(
                {"time": "This place has already been booked"}
            )


class PolymorphicBookingSerializer(MainPolymorphicSerializer):
    model_serializer_mapping = {
        OneTimeActivityBooking: OneTimeActivityBookingSerializer,
        RecurringActivityBooking: RecurringActivityBookingSerializer,
    }

    def _get_resource_type_from_mapping(self, mapping):
        activity_pk = mapping.get("activity_pk")
        if not activity_pk:
            raise serializers.ValidationError({"activity_pk": "The field is required"})

        activity_instance = Activity.objects.filter(pk=activity_pk).first()
        if not activity_instance:
            raise serializers.ValidationError(
                {"activity_pk": "The object is not found"}
            )

        activity_type = activity_instance.__class__.__name__
        activity_booking_mapping = {
            "OneTimeActivity": "OneTimeActivityBooking",
            "RecurringActivity": "RecurringActivityBooking",
        }
        return activity_booking_mapping[activity_type]
