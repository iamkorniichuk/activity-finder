from rest_framework import serializers
from django.contrib.gis.db.models import PointField as ModelPointField, Manager

from commons.models import TimeRangeField as ModelTimeRangeField
from files.models import File

from .utils import (
    add_choice_display_fields,
    add_current_user_serializer,
    add_fk_serializers,
    add_multiple_file_fields,
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

            multiple_file_fields = getattr(meta, "multiple_file_fields", None)
            if multiple_file_fields:
                attrs = add_multiple_file_fields(attrs, multiple_file_fields)

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

    def _save_multiple_file(self, instance, files):
        for field_name, files in files.items():
            objs = []
            for order, file in enumerate(files):
                objs.append(File(file=file, order=order))

            objs = File.objects.bulk_create(objs)
            getattr(instance, field_name).set(objs)

    def _pop_multiple_files(self, data):
        meta = getattr(self, "Meta", None)
        if meta is None:
            return

        multiple_file_fields = getattr(meta, "multiple_file_fields", None)
        if multiple_file_fields is None:
            return

        files = {}
        for field_name in multiple_file_fields.keys():
            file_field_name = field_name + "_files"
            if file_field_name in data:
                files[field_name] = data.pop(file_field_name)

        return files

    def create(self, validated_data):
        files = self._pop_multiple_files(validated_data)
        instance = super().create(validated_data)
        if files is not None:
            self._save_multiple_file(instance, files)
        return instance

    def update(self, instance, validated_data):
        files = self._pop_multiple_files(validated_data)
        instance = super().update(instance, validated_data)
        if files is not None:
            self._save_multiple_file(instance, files)
        return instance
