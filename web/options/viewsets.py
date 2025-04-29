from rest_framework import viewsets

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import OptionSerializer, Option


@with_my_list_endpoint(field_name="options", methods=["get"])
class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
