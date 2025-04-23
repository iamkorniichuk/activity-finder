from rest_framework import viewsets, mixins

from commons.viewsets import with_my_list_endpoint
from users.permissions import OwnedByCurrentUser

from .serializers import Reaction, ReactionSerializer


@with_my_list_endpoint(field_name="reactions", methods=["get"])
class ReactionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_permissions(self):
        return [OwnedByCurrentUser("created_by")]
