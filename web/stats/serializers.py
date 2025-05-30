from rest_framework import serializers
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth


class StatSerializer(serializers.Serializer):
    INTERVAL_CHOICES = [
        ("day", "day"),
        ("week", "week"),
        ("month", "month"),
    ]

    start = serializers.DateField()
    end = serializers.DateField()
    interval = serializers.ChoiceField(choices=INTERVAL_CHOICES)

    def validate(self, data):
        if data["start"] >= data["end"]:
            raise serializers.ValidationError(
                {"start": "Value needs to be smaller than `end`."}
            )
        return data

    def get_trunc_function(self):
        interval = self.validated_data.get("interval")

        return {
            "day": TruncDay,
            "week": TruncWeek,
            "month": TruncMonth,
        }[interval]
