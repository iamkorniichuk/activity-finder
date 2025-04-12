from rest_framework import viewsets, parsers

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import PolymorphicActivitySerializer
from .models import Activity


@with_my_list_endpoint(field_name="activities", methods=["get"])
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = PolymorphicActivitySerializer
    queryset = Activity.objects.all()
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
