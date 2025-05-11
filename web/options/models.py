from django.db import models

from commons.models import with_history
from activities.models import RecurringActivity
from users.models import User


@with_history()
class Option(models.Model):
    class Meta:
        default_related_name = "options"
        constraints = [
            models.UniqueConstraint(
                fields=("name", "activity"),
                condition=models.Q(is_current=True),
                name="unique_current_option_per_activity",
            )
        ]

    name = models.CharField(max_length=32)
    description = models.TextField()
    activity = models.ForeignKey(RecurringActivity, models.CASCADE)
    created_by = models.ForeignKey(User, models.PROTECT)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Option({self.name})"
