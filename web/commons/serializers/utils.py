from rest_framework import serializers
from rest_framework.utils.field_mapping import get_relation_kwargs
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from users.serializers import UserSerializer
from files.serializers import FileSerializer


def _add_fields(meta, *fields):
    if hasattr(meta, "fields"):
        fields_type = type(meta.fields)
        if not isinstance(fields, fields_type):
            fields = fields_type(fields)
        meta.fields += fields


def add_multiple_file_fields(attrs, multiple_file_fields, info):
    for serializer_field_name, extra_kwargs in multiple_file_fields.items():
        source = serializer_field_name
        files_field_name = serializer_field_name + "_files"

        attrs[serializer_field_name] = FileSerializer(
            many=True, read_only=True, required=False
        )

        files_field_kwargs = get_relation_kwargs(
            serializer_field_name, info.relations[source]
        )
        invalid_kwargs = ("view_name", "to_field", "source", "queryset", "many")
        for name in invalid_kwargs:
            files_field_kwargs.pop(name, None)

        attrs[files_field_name] = serializers.ListField(
            child=serializers.FileField(**extra_kwargs),
            write_only=True,
            **files_field_kwargs,
        )

        _add_fields(attrs["Meta"], serializer_field_name, files_field_name)

    return attrs


def add_fk_serializers(attrs, fk_serializers, info):
    for serializer_field_name, serializer_field in fk_serializers.items():
        pk_field_name = serializer_field_name + "_pk"
        source = serializer_field_name

        pk_field_kwargs = get_relation_kwargs(source, info.relations[source])
        invalid_kwargs = ("view_name", "to_field")
        for name in invalid_kwargs:
            pk_field_kwargs.pop(name, None)

        pk_field_kwargs["source"] = source

        pk_field = serializers.PrimaryKeyRelatedField(**pk_field_kwargs)

        attrs[serializer_field_name] = serializer_field(read_only=True, required=False)
        attrs[pk_field_name] = pk_field

        _add_fields(attrs["Meta"], serializer_field_name, pk_field_name)

    return attrs


def add_current_user_serializer(attrs, source):
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


def add_choice_display_fields(attrs, fields):
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
