from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import VenueSerializer, Venue


@with_my_list_endpoint(field_name="venues", methods=["get"])
class VenueViewSet(viewsets.ModelViewSet):
    serializer_class = VenueSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @action(["post"], detail=True)
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.is_publishable(instance):
            instance.is_published = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(
            "The object is not complete to be published.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(["post"], detail=True)
    def hide(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_published = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def is_publishable(self, instance):
        return len(instance.layouts.all()) > 0

    def get_queryset(self):
        filtering = Q(is_published=True)
        current_user = self.request.user
        if not current_user.is_anonymous:
            filtering = filtering | Q(created_by=current_user)

        return (
            Venue.objects.select_related("created_by")
            .prefetch_related("route", "media")
            .filter(filtering)
            .all()
        )

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
