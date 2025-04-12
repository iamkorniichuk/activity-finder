from activities.models.recurrings import RecurringActivity
from schedules.serializers import ScheduleSerializer

from .activities import ActivitySerializer


class RecurringActivitySerializer(ActivitySerializer):
    class Meta:
        model = RecurringActivity
        fields = (
            "pk",
            "name",
            "description",
            "media",
            "files",
            "location",
            "is_remote",
            "schedule",
            "duration",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"
        fk_serializers = {"schedule": ScheduleSerializer}
