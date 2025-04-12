from django.db import models

from commons.models import TimeRangeField

from .activities import Activity


class OneTimeActivity(Activity):
    class Meta:
        default_related_name = "one_time_activities"

    time_range = TimeRangeField()
    date = models.DateField()

    def __repr__(self):
        return f"OneTimeActivity({self.name})"
