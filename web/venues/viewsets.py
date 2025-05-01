from rest_framework import viewsets, parsers

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import VenueSerializer, Venue


@with_my_list_endpoint(field_name="venues", methods=["get"])
class VenueViewSet(viewsets.ModelViewSet):
    serializer_class = VenueSerializer
    queryset = (
        Venue.objects.select_related("created_by")
        .prefetch_related("route", "media")
        .all()
    )
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
