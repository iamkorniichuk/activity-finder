from django.db import models
from polymorphic.models import PolymorphicModel

from commons.models import FloatPairField
from venues.models import Venue
from users.models import User


class Layout(models.Model):
    class Meta:
        default_related_name = "layouts"
        unique_together = ("name", "venue")

    name = models.CharField(max_length=64)
    size = FloatPairField()
    venue = models.ForeignKey(Venue, models.CASCADE)
    created_by = models.ForeignKey(User, models.PROTECT)

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"Layout({self.pk})"


class VisualObject(PolymorphicModel):
    class Meta:
        default_related_name = "visual_objects"

    name = models.CharField(max_length=128)
    position = FloatPairField()
    size = FloatPairField()
    rotation = models.FloatField()
    layout = models.ForeignKey(Layout, models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"VisualObject({self.pk})"


class Seat(VisualObject):
    class Meta:
        default_related_name = "seats"

    def __repr__(self):
        return f"Seat({self.pk})"


class SeatZone(Seat):
    class Meta:
        default_related_name = "seat_zones"

    seat_amount = models.PositiveSmallIntegerField()

    def __repr__(self):
        return f"SeatZone({self.pk})"
