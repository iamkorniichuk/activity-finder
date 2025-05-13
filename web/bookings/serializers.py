from rest_framework import serializers

from commons.serializers import MainModelSerializer
from options.serializers import OptionSerializer

from .models import Booking


class BookingSerializer(MainModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "week_day", "time")
        read_only_fields = ("pk",)
        choice_display_fields = ("week_day",)


def within_time_range(time, time_range):
    return time >= time_range[0] and time < time_range[1]


class SensitiveBookingSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        fields = BookingSerializer.Meta.fields + (
            "booked_by",
            "booked_at",
            "option",
            "note",
        )
        current_user_field = "booked_by"
        fk_serializers = {
            "option": {"serializer": OptionSerializer},
        }

    def validate(self, data):
        option = data.get("option") or self.get_current("option")
        week_day = data.get("week_day") or self.get_current("week_day")
        time = data.get("time") or self.get_current("time")
        activity = option.activity
        schedule = activity.schedule

        self.validate_is_within_schedule(schedule, week_day, time)
        self.validate_is_booking_free(activity, week_day, time)

        return super().validate(data)

    def validate_is_within_schedule(self, schedule, week_day, time):
        for obj in schedule.work_days.all():
            day = obj.week_day
            if day == week_day:
                for slot in obj.slots:
                    if slot == time:
                        return

                raise serializers.ValidationError("Time doesn't suit the schedule")

        raise serializers.ValidationError("Week day doesn't suit the schedule")

    def validate_is_booking_free(self, activity, week_day, time):
        same_booking = Booking.objects.filter(
            option__activity__pk=activity["pk"], week_day=week_day, time=time
        )
        if same_booking.exists():
            raise serializers.ValidationError("This place has already been booked")
