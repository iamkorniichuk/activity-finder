from django.db import models
from django.utils.timezone import timedelta

from users.models import User


class TimeRange(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return str(self.start)

    def __repr__(self):
        return f"TimeRange({self.pk})"


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
    work_hours = models.ForeignKey(
        TimeRange,
        models.CASCADE,
        related_name="works",
    )
    break_hours = models.ManyToManyField(
        TimeRange,
        blank=True,
        related_name="breaks",
    )

    def __str__(self):
        return self.get_day_display()

    def __repr__(self):
        return f"WorkDay({self.pk})"


class Schedule(models.Model):
    class Meta:
        default_related_name = "schedules"

    work_days = models.ManyToManyField(WorkDay)
    booking_duration = models.DurationField(default=timedelta(hours=1))
    created_by = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return self.pk

    def __repr__(self):
        return f"Schedule({self.pk})"
