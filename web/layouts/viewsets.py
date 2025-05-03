from rest_framework import viewsets

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import Layout, LayoutSerializer


@with_my_list_endpoint(field_name="layouts", methods=["get"])
class LayoutViewSet(viewsets.ModelViewSet):
    queryset = Layout.objects.all()
    serializer_class = LayoutSerializer

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
