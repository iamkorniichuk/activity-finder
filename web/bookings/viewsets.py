from rest_framework import viewsets, mixins

from commons.viewsets import with_my_list_endpoint
from users.permissions import OwnedByCurrentUser

from .serializers import Booking, PolymorphicBookingSerializer


@with_my_list_endpoint(field_name="bookings", methods=["get"])
class BookingViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Booking.objects.select_related("booked_by").all()
    serializer_class = PolymorphicBookingSerializer

    def get_permissions(self):
        return [OwnedByCurrentUser("booked_by")]
