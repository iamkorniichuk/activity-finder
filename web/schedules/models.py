from django.db import models
from django.contrib.postgres.fields import ArrayField

from commons.models import TimeRangeField, WeekDayField
from users.models import User


class WorkDay(models.Model):
    week_day = WeekDayField()
    work_hours = TimeRangeField()
    break_hours = ArrayField(TimeRangeField(), blank=True, null=True)

    def __str__(self):
        return self.pk

    def __repr__(self):
        return f"WorkDay({self.pk})"


class Schedule(models.Model):
    class Meta:
        default_related_name = "schedules"

    work_days = models.ManyToManyField(WorkDay)
    booking_duration = models.DurationField()
    created_by = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return self.pk

    def __repr__(self):
        return f"Schedule({self.pk})"
