from rest_framework import viewsets, parsers
from django_filters import rest_framework as filters

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import PolymorphicActivitySerializer, Activity
from .filtersets import ActivityFilterSet


@with_my_list_endpoint(field_name="activities", methods=["get"])
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = PolymorphicActivitySerializer
    queryset = (
        Activity.objects.select_related("venue", "created_by")
        .prefetch_related("media")
        .all()
    )
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ActivityFilterSet

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
