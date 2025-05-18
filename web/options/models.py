from django.db import models

from activities.models import RecurringActivity
from users.models import User


class Option(models.Model):
    class Meta:
        default_related_name = "options"

    name = models.CharField(max_length=32)
    description = models.TextField()
    activity = models.ForeignKey(RecurringActivity, models.CASCADE)
    created_by = models.ForeignKey(User, models.PROTECT)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Option({self.name})"
