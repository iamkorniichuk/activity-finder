from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import datetime

from commons.models import TimeRangeField, WeekDayField, with_history
from users.models import User


def generate_slots(booking_duration, work_hours, break_hours):
    start, end = work_hours
    current = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)

    slots = []
    while current + booking_duration <= end_dt:
        current_time = current.time()
        if not any(
            datetime.combine(datetime.today(), bh_start)
            <= current
            < datetime.combine(datetime.today(), bh_end)
            for bh_start, bh_end in break_hours
        ):
            slots.append(current_time)
        current += booking_duration

    return slots


class WorkDay(models.Model):
    week_day = WeekDayField()
    work_hours = TimeRangeField()
    break_hours = ArrayField(TimeRangeField(), blank=True, null=True)
    slots = ArrayField(models.TimeField(), blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"WorkDay({self.pk})"


@with_history()
class Schedule(models.Model):
    class Meta:
        default_related_name = "schedules"

    work_days = models.ManyToManyField(WorkDay)
    booking_duration = models.DurationField()
    created_by = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"Schedule({self.pk})"
