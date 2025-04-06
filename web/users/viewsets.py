from rest_framework import viewsets, mixins, parsers

from commons.viewsets import with_my_object_endpoint

from .serializers import User, UserSerializer
from .permissions import OwnedByCurrentUserOrReadOnly


@with_my_object_endpoint(pk_field_name="pk", methods=["get", "put", "patch"])
class UserViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly()]
