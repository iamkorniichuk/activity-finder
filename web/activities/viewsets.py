from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django_filters import rest_framework as filters

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import PolymorphicActivitySerializer, Activity, OneTimeActivity
from .filtersets import ActivityFilterSet


@with_my_list_endpoint(field_name="activities", methods=["get"])
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = PolymorphicActivitySerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ActivityFilterSet

    @action(["post"], detail=True)
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_type = instance.__class__.__name__
        type_method_mapping = {
            "OneTimeActivity": self.is_one_time_activity_publishable,
            "RecurringActivity": self.is_recurring_activity_publishable,
        }
        is_publishable = type_method_mapping[instance_type](instance)
        if is_publishable:
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

    def is_recurring_activity_publishable(self, instance):
        return len(instance.options.all()) > 0

    def is_one_time_activity_publishable(self, instance):
        return True

    def get_queryset(self):
        is_published = Q(is_published=True)
        today = timezone.now().date()
        is_relevant = Q(OneTimeActivity___date__gt=today) | ~Q(
            instance_of=OneTimeActivity
        )
        current_user = self.request.user
        is_mine = Q(created_by=current_user)

        all_filters = is_published
        if self.action != "retrieve":
            all_filters &= is_relevant
        if not current_user.is_anonymous:
            all_filters |= is_mine

        return (
            Activity.objects.select_related("venue", "created_by")
            .prefetch_related("media")
            .filter(all_filters)
            .all()
        )

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
