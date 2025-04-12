from activities.models.one_times import OneTimeActivity

from .activities import ActivitySerializer


class OneTimeActivitySerializer(ActivitySerializer):
    class Meta:
        model = OneTimeActivity
        fields = (
            "pk",
            "name",
            "description",
            "media",
            "files",
            "location",
            "is_remote",
            "time_range",
            "date",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"
