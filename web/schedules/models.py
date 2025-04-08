from django.db import models
from django.contrib.postgres.fields import ArrayField

from commons.models import TimeRangeField
from users.models import User


class WorkDay(models.Model):
    class WeekDayChoices(models.IntegerChoices):
        MONDAY = 0, "monday"
        TUESDAY = 1, "tuesday"
        WEDNESDAY = 2, "wednesday"
        THURSDAY = 3, "thursday"
        FRIDAY = 4, "friday"
        SATURDAY = 5, "saturday"
        SUNDAY = 6, "sunday"

    day = models.PositiveSmallIntegerField(choices=WeekDayChoices.choices)
    work_hours = TimeRangeField()
    break_hours = ArrayField(TimeRangeField(), blank=True, null=True)

    def __str__(self):
        return self.get_day_display()

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
