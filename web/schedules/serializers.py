from rest_framework import serializers

from commons.serializers import MainWritableNestedModelSerializer

from .models import Schedule, WorkDay


class WorkDaySerializer(MainWritableNestedModelSerializer):
    class Meta:
        model = WorkDay
        fields = ("week_day", "work_hours", "break_hours", "slots")
        choice_fields = ("week_day",)
        read_only_fields = ("slots",)


class ScheduleSerializer(MainWritableNestedModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "pk",
            "work_days",
            "booking_duration",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"

    work_days = WorkDaySerializer(many=True)

    def validate_work_days(self, data):
        unique_days = set([obj["week_day"] for obj in data])
        if len(unique_days) < len(data):
            raise serializers.ValidationError("Each day needs to be unique")
        return data

    def validate(self, data):
        booking_duration = data.get("booking_duration") or self.get_current(
            "booking_duration"
        )
        work_days = data.get("work_days") or self.get_current("work_days")

        for day in work_days:
            work_hours = day["work_hours"]
            break_hours = day.get("break_hours")
            # Handling when `break_hours` is missing and when it's `None`
            if break_hours is None:
                break_hours = []

            self.validate_divisible_hours(booking_duration, work_hours, break_hours)

        return data

    def validate_divisible_hours(self, booking_duration, work_hours, break_hours):
        work_start, work_end = work_hours
        break_hours.append([work_end, None])

        for break_start, break_end in break_hours:
            work_end = break_start

            delta = time_difference(work_start, work_end)
            if delta % booking_duration.total_seconds() != 0:
                raise serializers.ValidationError(
                    {
                        "work_days": f"Interval {work_start}-{work_end} is not divisible by `booking_duration`."
                    }
                )

            work_start = break_end


def time_difference(minuend, subtrahend):
    hours = (subtrahend.hour - minuend.hour) * 60 * 60
    minutes = (subtrahend.minute - minuend.minute) * 60
    seconds = subtrahend.second - minuend.second
    return hours + minutes + seconds
