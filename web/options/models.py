from django.db import models

from activities.models import Activity
from users.models import User


class Option(models.Model):
    class Meta:
        default_related_name = "options"
        unique_together = ("name", "activity")

    name = models.CharField(max_length=32)
    description = models.TextField()
    activity = models.ForeignKey(Activity, models.CASCADE)
    created_by = models.ForeignKey(User, models.PROTECT)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Option({self.name})"
