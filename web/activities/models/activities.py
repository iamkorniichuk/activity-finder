from django.contrib.gis.db import models
from polymorphic.models import PolymorphicModel

from users.models import User


class Activity(PolymorphicModel):
    class Meta:
        default_related_name = "activities"

    name = models.CharField(max_length=64)
    description = models.TextField()
    created_by = models.ForeignKey(User, models.CASCADE)
    is_remote = models.BooleanField()
    location = models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Activity({self.name})"


class ActivityMedia(models.Model):
    class Meta:
        ordering = ["order"]

    activity = models.ForeignKey(Activity, models.CASCADE, related_name="media")
    file = models.FileField(upload_to="activities/")
    order = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk

    def __repr__(self):
        return f"ActivityMedia({self.pk})"
