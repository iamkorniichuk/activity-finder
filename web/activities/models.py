from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from polymorphic.models import PolymorphicModel

from users.models import User
from venues.models import Venue
from layouts.models import Layout
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
    venue = models.ForeignKey(Venue, models.PROTECT)
    media = models.ManyToManyField(File)
    is_published = models.BooleanField(default=False, blank=True, editable=False)
    website_links = ArrayField(models.URLField(), size=10, blank=True, default=list)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Activity({self.name})"


class OneTimeActivity(Activity):
    class Meta(Activity.Meta):
        default_related_name = "one_time_activities"

    time_range = TimeRangeField()
    layout = models.ForeignKey(Layout, models.PROTECT)
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
