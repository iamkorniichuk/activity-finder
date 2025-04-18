from django.contrib.gis.db import models
from polymorphic.models import PolymorphicModel

from users.models import User
from commons.models import TimeRangeField
from schedules.models import Schedule
from files.models import File


class Activity(PolymorphicModel):
    class Meta:
        default_related_name = "activities"

    name = models.CharField(max_length=64)
    description = models.TextField()
    created_by = models.ForeignKey(User, models.CASCADE)
    location = models.PointField(srid=4326, null=True, blank=True)
    is_remote = models.BooleanField()
    media = models.ManyToManyField(File)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Activity({self.name})"


class OneTimeActivity(Activity):
    class Meta:
        default_related_name = "one_time_activities"

    time_range = TimeRangeField()
    date = models.DateField()

    def __repr__(self):
        return f"OneTimeActivity({self.name})"


class RecurringActivity(Activity):
    class Meta:
        default_related_name = "recurring_activities"

    schedule = models.ForeignKey(Schedule, models.CASCADE)
    duration = models.DurationField()

    def __repr__(self):
        return f"RecurringActivity({self.name})"
