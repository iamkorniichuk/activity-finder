from django.contrib.gis.db import models
from polymorphic.models import PolymorphicModel

from users.models import User
from venues.models import Venue
from commons.models import TimeRangeField
from schedules.models import Schedule
from files.models import File


class Activity(PolymorphicModel):
    class Meta:
        default_related_name = "activities"
        ordering = ["name", "pk"]

    name = models.CharField(max_length=64)
    description = models.TextField()
    created_by = models.ForeignKey(User, models.CASCADE)
    venue = models.ForeignKey(Venue, models.PROTECT, null=True, blank=True)
    is_remote = models.BooleanField()
    media = models.ManyToManyField(File)
    is_published = models.BooleanField(default=False, blank=True, editable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Activity({self.name})"


class OneTimeActivity(Activity):
    class Meta(Activity.Meta):
        default_related_name = "one_time_activities"

    time_range = TimeRangeField()
    date = models.DateField()

    def __repr__(self):
        return f"OneTimeActivity({self.name})"


class RecurringActivity(Activity):
    class Meta(Activity.Meta):
        default_related_name = "recurring_activities"

    schedule = models.ForeignKey(Schedule, models.CASCADE, related_name="activities")
    duration = models.DurationField()

    def __repr__(self):
        return f"RecurringActivity({self.name})"
