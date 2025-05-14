from django.db import models


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
