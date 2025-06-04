from copy import copy
from typing import Optional
from rest_framework import serializers
from django.utils.timezone import timedelta, now, datetime
from django.db.models import ExpressionWrapper, F, DateTimeField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from commons.serializers import MainWritableNestedModelSerializer
from commons.time import TimeWrapper

from .models import Schedule, WorkDay, generate_slots


class SlotSerializer(serializers.Serializer):
    time = serializers.TimeField()
    is_booked = serializers.SerializerMethodField()

    @extend_schema_field(Optional[OpenApiTypes.BOOL])
    def get_is_booked(self, obj):
        pass


class WorkDaySerializer(MainWritableNestedModelSerializer):
    class Meta:
        model = WorkDay
        fields = ("week_day", "work_hours", "break_hours", "slots", "date")
        choice_fields = ("week_day",)
        read_only_fields = ("slots",)

    slots = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    @extend_schema_field(SlotSerializer)
    def get_slots(self, instance):
        activity = self.context.get("activity")
        if not activity:
            return [{"time": slot, "is_booked": None} for slot in instance.slots]

        from bookings.models import RecurringActivityBooking

        booking_duration = activity.schedule.booking_duration
        date = self.get_date(instance)

        slot_intervals = {
            slot: (
                datetime.combine(date, slot),
                datetime.combine(date, slot) + booking_duration,
            )
            for slot in instance.slots
        }

        same_day_bookings = (
            RecurringActivityBooking.objects.filter(
                activity=activity,
                date=date,
            )
            .annotate(
                start=ExpressionWrapper(
                    F("date") + F("time"), output_field=DateTimeField()
                )
            )
            .annotate(
                end=ExpressionWrapper(
                    F("start") + booking_duration, output_field=DateTimeField()
                ),
            )
        ).all()

        booked_intervals = [(b.start, b.end) for b in same_day_bookings]

        results = []
        for slot, (slot_start, slot_end) in slot_intervals.items():
            is_booked = any(
                booking_start < slot_end and booking_end > slot_start
                for booking_start, booking_end in booked_intervals
            )
            results.append({"time": slot, "is_booked": is_booked})

        return results

    @extend_schema_field(Optional[OpenApiTypes.DATE])
    def get_date(self, instance):
        activity = self.context.get("activity")
        if not activity:
            return None

        today = now()
        monday = today - timedelta(days=today.weekday())
        datetime = monday + timedelta(days=instance.week_day)
        return datetime.date()

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
            "activities",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"

    work_days = WorkDaySerializer(many=True)

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        # Ensure `work_days.slots` recalculation
        is_update_action = instance is not None and data is not serializers.empty
        if is_update_action and "work_days" not in data:
            self.parent = None  # Avoid `AttributeError`
            field = self.fields["work_days"]
            work_days = field.get_attribute(instance)
            data["work_days"] = field.to_representation(work_days)
        super().__init__(instance, data, **kwargs)

    def to_representation(self, instance):
        self.fields["work_days"].context["activity"] = self.context.get("activity")
        return super().to_representation(instance)

    def get_fields(self):
        from activities.serializers import PolymorphicActivitySerializer

        fields = super().get_fields()
        fields["activities"] = PolymorphicActivitySerializer(
            many=True,
            read_only=True,
        )
        return fields

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
