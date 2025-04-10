from commons.serializers import MainModelSerializer

from .models import Territory


class TerritorySerializer(MainModelSerializer):
    class Meta:
        model = Territory
        fields = (
            "id",
            "code",
            "name",
            "type",
            "upper_level",
        )
        choice_fields = ("type",)

    def get_fields(self):
        fields = super(TerritorySerializer, self).get_fields()
        fields["upper_level"] = TerritorySerializer()
        return fields


class AutocompleteTerritorySerializer(MainModelSerializer):
    class Meta:
        model = Territory
        fields = ("name",)
