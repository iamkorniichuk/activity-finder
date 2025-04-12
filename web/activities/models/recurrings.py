from django.db import models

from schedules.models import Schedule

from .activities import Activity


class RecurringActivity(Activity):
    class Meta:
        default_related_name = "recurring_activities"

    schedule = models.ForeignKey(Schedule, models.CASCADE)
    duration = models.DurationField()

    def __repr__(self):
        return f"RecurringActivity({self.name})"
