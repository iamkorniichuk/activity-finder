from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .one_times import OneTimeActivitySerializer, OneTimeActivity
from .recurrings import RecurringActivitySerializer, RecurringActivity


class PolymorphicActivitySerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        OneTimeActivity: OneTimeActivitySerializer,
        RecurringActivity: RecurringActivitySerializer,
    }
    resource_type_field_name = "type"

    def run_validation(self, data):
        if self.instance and self.resource_type_field_name in data:
            new_type = self._get_resource_type_from_mapping(data)
            old_type = self.instance.__class__.__name__
            if new_type != old_type:
                raise serializers.ValidationError(
                    {
                        self.resource_type_field_name: "You can't change `type` on created activity."
                    }
                )
        return super().run_validation(data)
