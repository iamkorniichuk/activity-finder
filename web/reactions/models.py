from django.db import models

from activities.models import Activity
from users.models import User


class Reaction(models.Model):
    class Meta:
        default_related_name = "reactions"
        unique_together = ("activity", "created_by")

    class TypeChoices(models.TextChoices):
        LIKE = "like", "Like"
        DISLIKE = "dislike", "Dislike"

    activity = models.ForeignKey(Activity, models.CASCADE)
    created_by = models.ForeignKey(User, models.CASCADE)
    type = models.CharField(max_length=16, choices=TypeChoices.choices)

    def __str__(self):
        return self.pk

    def __repr__(self):
        return f"Reaction({self.pk})"
