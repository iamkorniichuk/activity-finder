from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from .lookups import StartTransform, EndTransform, DurationTransform


class TimeRangeField(ArrayField):
    def __init__(self, *args, **kwargs):
        kwargs["base_field"] = models.TimeField()
        kwargs["size"] = 2
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        start, end = value
        if start >= end:
            raise ValidationError("`end` value must be greater than `start` value.")

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        self.model._meta.get_field(name).register_lookup(StartTransform)
        self.model._meta.get_field(name).register_lookup(EndTransform)
        self.model._meta.get_field(name).register_lookup(DurationTransform)


class FloatPairField(ArrayField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        kwargs["base_field"] = models.FloatField()
        kwargs["size"] = 2
        super().__init__(*args, **kwargs)


class WeekDayChoices(models.IntegerChoices):
    MONDAY = 0, "monday"
    TUESDAY = 1, "tuesday"
    WEDNESDAY = 2, "wednesday"
    THURSDAY = 3, "thursday"
    FRIDAY = 4, "friday"
    SATURDAY = 5, "saturday"
    SUNDAY = 6, "sunday"


class WeekDayField(models.PositiveSmallIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = WeekDayChoices.choices
        super().__init__(*args, **kwargs)
