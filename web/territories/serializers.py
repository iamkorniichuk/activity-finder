from rest_framework import serializers

from .models import Territory


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = (
            "id",
            "code",
            "name",
            "type",
            "type_label",
            "upper_level",
        )

    type_label = serializers.SerializerMethodField()

    def get_type_label(self, obj):
        return obj.get_type_display()

    def get_fields(self):
        fields = super(TerritorySerializer, self).get_fields()
        fields["upper_level"] = TerritorySerializer()
        return fields


class AutocompleteTerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = ("name",)
