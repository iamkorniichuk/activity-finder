from rest_framework import serializers

from commons.serializers import MainWritableNestedModelSerializer

from .models import Schedule, WorkDay


class WorkDaySerializer(MainWritableNestedModelSerializer):
    class Meta:
        model = WorkDay
        fields = ("day", "work_hours", "break_hours")
        choice_fields = ("day",)


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
        unique_days = set([obj["day"] for obj in data])
        if len(unique_days) < len(data):
            raise serializers.ValidationError("Each day needs to be unique")
        return data

    def validate(self, data):
        duration = self.get_current("booking_duration", data)

        for day in self.get_current("work_days", data):
            work_start, work_end = day["work_hours"]

            breaks = day.get("break_hours")
            # Handle `None` instance's value and missing value in request
            if breaks is None:
                breaks = []
            breaks.append([work_end, None])

            for break_start, break_end in breaks:
                work_end = break_start

                delta = time_difference(work_start, work_end)
                if delta % duration.total_seconds() != 0:
                    raise serializers.ValidationError(
                        {
                            "work_days": f"Interval {work_start}-{work_end} is not divisible by `booking_duration`."
                        }
                    )

                work_start = break_end

        return data


def time_difference(minuend, subtrahend):
    hours = (subtrahend.hour - minuend.hour) * 60 * 60
    minutes = (subtrahend.minute - minuend.minute) * 60
    seconds = subtrahend.second - minuend.second
    return hours + minutes + seconds
