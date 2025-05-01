from rest_framework import viewsets

from users.permissions import OwnedByCurrentUserOrReadOnly
from commons.viewsets import with_my_list_endpoint

from .serializers import Schedule, ScheduleSerializer


@with_my_list_endpoint(field_name="schedules", methods=["get"])
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = (
        Schedule.objects.select_related("created_by")
        .prefetch_related("work_days")
        .all()
    )
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        return [OwnedByCurrentUserOrReadOnly("created_by")]
