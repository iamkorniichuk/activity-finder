from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


@extend_schema_field(
    {
        "type": "string",
        "description": "Time range in `HH:MM[:SS]-HH:MM[:SS]` format.",
    }
)
class TimeRangeField(serializers.ListField):
    child = serializers.TimeField()
    min_length = 2
    max_length = 2

    def to_representation(self, data):
        representations = []
        for obj in data:
            representations.append(self.child.to_representation(obj))
        return "-".join(representations)

    def to_internal_value(self, data):
        data = data.split("-")
        return super().to_internal_value(data)
