from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.gis.db.models import PointField as ModelPointField, Manager

from commons.models import TimeRangeField as ModelTimeRangeField

from .utils import (
    add_choice_display_fields,
    add_current_user_serializer,
    add_fk_serializers,
)
from .fields import TimeRangeField, PointField


class MainModelSerializerMetaclass(serializers.SerializerMetaclass):
    def __new__(cls, name, bases, attrs):
        meta = attrs.get("Meta", None)
        if meta:
            current_user_field = getattr(meta, "current_user_field", None)
            if current_user_field:
                attrs = add_current_user_serializer(attrs, current_user_field)

            choice_fields = getattr(meta, "choice_fields", None)
            if choice_fields:
                attrs = add_choice_display_fields(attrs, choice_fields)

            fk_serializers = getattr(meta, "fk_serializers", None)
            if fk_serializers:
                attrs = add_fk_serializers(attrs, fk_serializers)

        return super().__new__(cls, name, bases, attrs)


class MainModelSerializerMixin:
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping[ModelTimeRangeField] = TimeRangeField
        self.serializer_field_mapping[ModelPointField] = PointField
        super().__init__(*args, **kwargs)

    def get_current(self, key, data):
        if key in data:
            return data[key]

        if key in self.initial_data:
            return self.initial_data[key]

        if self.instance:
            field = self.fields[key]
            value = field.get_attribute(self.instance)
            if isinstance(value, Manager):
                value = value.all()
            return field.to_internal_value(field.to_representation(value))


class MainModelSerializer(
    MainModelSerializerMixin,
    serializers.ModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    pass


class MainWritableNestedModelSerializer(
    MainModelSerializerMixin,
    WritableNestedModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    pass
