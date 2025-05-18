from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer

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
    - `multiple_file_fields` takes a dict `{"<field_name>": <extra_file_field_kwargs>}` and makes set fields to work for multiple file upload
    """

    pass


class MainWritableNestedModelSerializer(
    MainModelSerializerMixin,
    WritableNestedModelSerializer,
    metaclass=MainModelSerializerMetaclass,
):
    pass


class MainPolymorphicSerializer(PolymorphicSerializer):
    """
    Forbids changing the type on already created objects.
    """

    def run_validation(self, data):
        if self.instance and self.resource_type_field_name in data:
            new_type = self._get_resource_type_from_mapping(data)
            old_type = self.instance.__class__.__name__
            if new_type != old_type:
                raise serializers.ValidationError(
                    {
                        self.resource_type_field_name: f"You can't change `{self.resource_type_field_name}` on created activity."
                    }
                )
        return super().run_validation(data)
