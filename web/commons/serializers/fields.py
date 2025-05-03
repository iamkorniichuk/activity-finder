from rest_framework import serializers
from django.contrib.gis.geos import Point
from drf_spectacular.utils import extend_schema_field


@extend_schema_field(
    {
        "type": "string",
        "description": "Coordinates in `-12.95432,25.43335` format.",
    }
)
class PointField(serializers.Field):
    def __init__(self, precision=6, dimension=None, *args, **kwargs):
        self.precision = precision
        self.dimension = dimension
        super().__init__(*args, **kwargs)
        self.error_messages["dimension"] = (
            "Invalid coordinate's dimension. Expected: {dimension}."
        )

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        if self.dimension is None:
            model_field = getattr(parent.Meta.model, field_name).field
            self.dimension = model_field.dim

    def to_representation(self, value):
        if not isinstance(value, Point):
            return None

        representation = [str(round(value, self.precision)) for value in value.coords]
        return ",".join(representation)

    def to_internal_value(self, data):
        if data is None:
            return None

        data = [float(value) for value in data.split(",")]
        if len(data) != self.dimension:
            self.fail("dimension", dimension=self.dimension)

        return Point(data)


class PairField(serializers.ListField):
    separator = None
    child = None

    min_length = 2
    max_length = 2

    def to_representation(self, data):
        representations = []
        for obj in data:
            result = self.child.to_representation(obj)
            representations.append(str(result))
        return self.separator.join(representations)

    def to_internal_value(self, data: str):
        if isinstance(data, list):
            data = data[0]
        data = [obj.strip() for obj in data.split(self.separator)]
        return super().to_internal_value(data)


@extend_schema_field(
    {
        "type": "string",
        "description": "Time range in `HH:MM[:SS]-HH:MM[:SS]` format.",
    }
)
class TimeRangeField(PairField):
    child = serializers.TimeField()
    separator = "-"


class FloatPairField(PairField):
    separator = ","

    def __init__(self, **kwargs):
        self.min_value = kwargs.pop("min_value", None)
        self.max_value = kwargs.pop("max_value", None)
        kwargs["child"] = serializers.FloatField(
            min_value=self.min_value, max_value=self.max_value
        )
        super().__init__(**kwargs)
