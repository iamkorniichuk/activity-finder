from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.serializers import UserSerializer

from .models import Schedule, WorkDay, TimeRange


class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = ("pk", "start", "end")
        read_only_fields = ("pk",)

    def validate(self, data):
        start = data["start"]
        end = data["end"]
        if start >= end:
            raise serializers.ValidationError(
                {"start": "The field needs to be less than end field"}
            )
        return data


class WorkDaySerializer(WritableNestedModelSerializer):
    class Meta:
        model = WorkDay
        fields = ("pk", "day", "work_hours", "break_hours")
        read_only_fields = ("pk",)

    work_hours = TimeRangeSerializer()
    break_hours = TimeRangeSerializer(many=True, allow_null=True, required=False)


class ScheduleSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "pk",
            "work_days",
            "booking_duration",
            "created_by",
            "created_by_pk",
        )
        read_only_fields = ("pk",)

    work_days = WorkDaySerializer(many=True)
    created_by = UserSerializer(read_only=True, required=False)
    created_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="created_by",
    )

    def validate_work_days(self, data):
        unique_days = set([obj["day"] for obj in data])
        if len(unique_days) < len(data):
            raise serializers.ValidationError("Each day needs to be unique")
        return data

    def validate(self, data):
        duration = data["booking_duration"]

        for day in data["work_days"]:
            hours = day["work_hours"]
            breaks = day["break_hours"]
            breaks.append({"start": hours["end"]})

            start = hours["start"]

            for obj in breaks:
                end = obj["start"]
                delta = time_difference(end, start)
                if delta % duration.total_seconds() != 0:
                    raise serializers.ValidationError(
                        {
                            "work_days": f"Interval {start}-{end} is not divisible by `booking_duration`."
                        }
                    )

                start = obj["end"]

        return data


def time_difference(minuend, subtrahend):
    hours = (subtrahend.hour - minuend.hour) * 60 * 60
    minutes = (subtrahend.minute - minuend.minute) * 60
    seconds = subtrahend.second - minuend.second
    return hours + minutes + seconds
