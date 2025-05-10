from django.contrib.gis.db import models

from commons.models import with_history
from users.models import User
from files.models import File


@with_history()
class Venue(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    route = models.ManyToManyField(
        File,
        related_name="route_venues",
        blank=True,
    )
    location = models.PointField(srid=4326)
    created_by = models.ForeignKey(User, models.PROTECT, related_name="venues")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    media = models.ManyToManyField(File, related_name="media_venues")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Venue({self.name})"
