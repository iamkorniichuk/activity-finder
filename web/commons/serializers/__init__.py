from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .mixins import MainModelSerializerMixin, MainModelSerializerMetaclass


class MainModelSerializer(
    MainModelSerializerMixin,
    serializers.ModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    """
    Adds new attributes to `Meta`:
    - `current_user_field` takes a field and implicitly sets its value to current user's model
    - `choice_display_fields` takes a list of fields and adds `<name>_display` read-only field pair to each of them
    - `fk_serializers` takes a dict `{"<field_name>": {"serializer": <serializer_class>}, **extra_kwargs}` and creates `<name>_pk` field pair that expects pk

    Attributes that need `MainModelSerializerMixin` to work:
    - `multiple_file_fields` takes a dict `{"<field_name>": <extra_file_field_kwargs>}` and makes set fields to work for multiple file upload
    """

    pass


class MainWritableNestedModelSerializer(
    MainModelSerializerMixin,
    WritableNestedModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    """
    Adds new attributes to `Meta`:
    - `current_user_field` takes a field and implicitly sets its value to current user's model
    - `choice_display_fields` takes a list of fields and adds `<name>_display` read-only field pair to each of them
    - `fk_serializers` takes a dict `{"<field_name>": {"serializer": <serializer_class>}, **extra_kwargs}` and creates `<name>_pk` field pair that expects pk

    Attributes that need `MainModelSerializerMixin` to work:
    - `multiple_file_fields` takes a dict `{"<field_name>": <extra_file_field_kwargs>}` and makes set fields to work for multiple file upload
    """

    pass
