from django.db import models

from users.models import User
from commons.models import WeekDayField
from options.models import Option


class Booking(models.Model):
    class Meta:
        default_related_name = "bookings"
        ordering = ["booked_at", "pk"]

    booked_by = models.ForeignKey(User, models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    option = models.ForeignKey(Option, models.PROTECT)
    week_day = WeekDayField()
    time = models.TimeField()
    note = models.TextField(blank=True, default="")

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"Booking({self.pk})"
