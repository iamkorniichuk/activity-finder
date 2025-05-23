from django.db import models
from polymorphic.models import PolymorphicModel

from users.models import User
from commons.models import WeekDayField
from options.models import Option
from layouts.models import Seat
from activities.models import Activity


class Booking(PolymorphicModel):
    class Meta:
        default_related_name = "bookings"
        ordering = ["booked_at", "activity", "pk"]

    activity = models.ForeignKey(Activity, models.PROTECT)
    booked_by = models.ForeignKey(User, models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"Booking({self.pk})"


class OneTimeActivityBooking(Booking):
    class Meta(Booking.Meta):
        default_related_name = "one_time_activity_bookings"

    seat = models.ForeignKey(Seat, models.PROTECT)

    def __repr__(self):
        return f"OneTimeActivityBooking({self.pk})"


class RecurringActivityBooking(Booking):
    class Meta(Booking.Meta):
        default_related_name = "recurring_activity_bookings"

    option = models.ForeignKey(Option, models.PROTECT)
    week_day = WeekDayField()
    time = models.TimeField()
    note = models.TextField(blank=True, default="")

    def __repr__(self):
        return f"RecurringActivityBooking({self.pk})"
