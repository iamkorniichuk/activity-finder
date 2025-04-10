from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes
from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.serializers import UserSerializer

from . import models


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


class MainModelSerializerMetaclass(serializers.SerializerMetaclass):
    def __new__(cls, name, bases, attrs):
        meta = attrs.get("Meta", None)
        if meta:
            current_user_field = getattr(meta, "current_user_field", None)
            if current_user_field:
                attrs = _add_current_user_serializer(attrs, current_user_field)

            choice_fields = getattr(meta, "choice_fields", None)
            if choice_fields:
                attrs = _add_choice_display_fields(attrs, choice_fields)

            fk_serializers = getattr(meta, "fk_serializers", None)
            if fk_serializers:
                attrs = _add_fk_serializers(attrs, fk_serializers)

        return super().__new__(cls, name, bases, attrs)


class MainModelSerializer(
    serializers.ModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping[models.TimeRangeField] = TimeRangeField
        super().__init__(*args, **kwargs)


class MainWritableNestedModelSerializer(
    WritableNestedModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping[models.TimeRangeField] = TimeRangeField
        super().__init__(*args, **kwargs)


def _add_fields(meta, *fields):
    if hasattr(meta, "fields"):
        fields_type = type(meta.fields)
        if not isinstance(fields, fields_type):
            fields = fields_type(fields)
        meta.fields += fields


def _add_fk_serializers(attrs, fk_serializers):
    for serializer_field_name, serializer_field in fk_serializers.items():
        pk_field_name = serializer_field_name + "_pk"
        source = serializer_field_name
        queryset = serializer_field.Meta.model.objects.all()

        pk_field = serializers.PrimaryKeyRelatedField(
            queryset=queryset,
            source=source,
        )
        attrs[serializer_field_name] = serializer_field(read_only=True, required=False)
        attrs[pk_field_name] = pk_field

        _add_fields(attrs["Meta"], serializer_field_name, pk_field_name)

    return attrs


def _add_current_user_serializer(attrs, source):
    serializer_field_name = source
    pk_field_name = source + "_pk"

    serializer_field = UserSerializer(read_only=True, required=False)
    pk_field = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source=source,
    )
    attrs[serializer_field_name] = serializer_field
    attrs[pk_field_name] = pk_field

    _add_fields(attrs["Meta"], serializer_field_name, pk_field_name)

    return attrs


def _add_choice_display_fields(attrs, fields):
    for name in fields:
        display_property_name = f"{name}_display"
        attrs[display_property_name] = serializers.SerializerMethodField()

        display_method_name = f"get_{display_property_name}"

        def method(self, obj):
            return getattr(obj, display_method_name)()

        method.__name__ = display_method_name
        attrs[display_method_name] = extend_schema_field(OpenApiTypes.STR)(method)

        _add_fields(attrs["Meta"], display_property_name)

    return attrs
