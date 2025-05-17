from copy import copy
from rest_framework import serializers

from commons.serializers import MainWritableNestedModelSerializer
from commons.time import TimeWrapper

from .models import Schedule, WorkDay, generate_slots


class WorkDaySerializer(MainWritableNestedModelSerializer):
    class Meta:
        model = WorkDay
        fields = ("week_day", "work_hours", "break_hours", "slots")
        choice_fields = ("week_day",)
        read_only_fields = ("slots",)

    def validate(self, data):
        booking_duration = self.context.get("booking_duration")
        if booking_duration is not None:
            work_hours = data.get("work_hours")
            break_hours = data.get("break_hours", [])
            data["slots"] = generate_slots(booking_duration, work_hours, break_hours)
        return data


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
        history_deep_copy_fields = ("work_days",)

    work_days = WorkDaySerializer(many=True)

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        # Ensure `work_days.slots` recalculation
        is_update_action = instance is not None and data is not serializers.empty
        if is_update_action and "work_days" not in data:
            value = self.fields["work_days"].get_attribute(instance)
            data["work_days"] = self.fields["work_days"].to_representation(value)
        super().__init__(instance, data, **kwargs)

    def validate_work_days(self, data):
        unique_days = set([obj["week_day"] for obj in data])
        if len(unique_days) < len(data):
            raise serializers.ValidationError("Each day needs to be unique")
        return data

    def validate(self, data):
        booking_duration = data.get("booking_duration") or self.get_current(
            "booking_duration"
        )
        self.context["booking_duration"] = booking_duration
        work_days = data.get("work_days") or self.get_current("work_days")

        for obj in work_days:
            work_hours = obj["work_hours"]
            break_hours = obj.get("break_hours", [])
            self.validate_divisible_hours(booking_duration, work_hours, break_hours)

        return data

    def validate_divisible_hours(self, booking_duration, work_hours, break_hours):
        work_hours = copy(work_hours)
        break_hours = copy(break_hours)

        work_start, work_end = work_hours
        break_hours.append([work_end, None])

        for break_start, break_end in break_hours:
            work_end = TimeWrapper(break_start)

            difference = work_end - work_start
            if difference.total_seconds() % booking_duration.total_seconds() != 0:
                raise serializers.ValidationError(
                    {
                        "work_days": f"Interval {work_start}-{work_end} is not divisible by `booking_duration`."
                    }
                )

            work_start = break_end
