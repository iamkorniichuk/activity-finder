from copy import copy
from django.db import models
from django.contrib.postgres.fields import ArrayField

from commons.models import TimeRangeField, WeekDayField
from commons.time import TimeWrapper
from users.models import User


def generate_slots(booking_duration, work_hours, break_hours):
    work_hours = copy(work_hours)
    break_hours = copy(break_hours)

    work_start, work_end = work_hours
    break_hours.append([work_end, None])

    slots = []
    for break_start, break_end in break_hours:
        if work_start is None:
            break

        current = TimeWrapper(work_start)
        while current < break_start:
            slots.append(current)
            current = current + booking_duration
        work_start = break_end

    return slots


class Schedule(models.Model):
    class Meta:
        default_related_name = "schedules"
        ordering = ["pk"]

    booking_duration = models.DurationField()
    created_by = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"Schedule({self.pk})"


class WorkDay(models.Model):
    class Meta:
        default_related_name = "work_days"
        ordering = ["week_day"]

    schedule = models.ForeignKey(Schedule, models.CASCADE)
    week_day = WeekDayField()
    work_hours = TimeRangeField()
    break_hours = ArrayField(TimeRangeField(), blank=True, default=list)
    slots = ArrayField(models.TimeField())

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"WorkDay({self.pk})"
