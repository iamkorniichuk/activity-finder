from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .mixins import MainModelSerializerMixin, MainModelSerializerMetaclass


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
