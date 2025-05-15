from django.core.validators import EMPTY_VALUES
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django_filters import rest_framework as filters

from territories.models import Territory

from .models import Activity


class SearchFilter(filters.CharFilter):
    def __init__(self, fields, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_fields = fields

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        qs = qs.annotate(search=SearchVector(*self.search_fields))
        return qs.filter(search=value)


def subclasses_as_choices(base_cls):
    choices = [(subclass.__name__, subclass) for subclass in base_cls.__subclasses__()]
    return choices


class ActivityFilterSet(filters.FilterSet):
    class Meta:
        model = Activity
        fields = ("name", "is_remote")

    search = SearchFilter(fields=("name", "description"))
    type = filters.MultipleChoiceFilter(
        method="filter_by_type",
        choices=subclasses_as_choices(Activity),
    )
    within_territory = filters.ModelChoiceFilter(
        method="filter_by_within_territory",
        queryset=Territory.objects.all(),
    )

    def filter_by_type(self, queryset, key, value):
        valid_choices = subclasses_as_choices(Activity)
        selected = [cls for name, cls in valid_choices if name in value]
        return queryset.instance_of(*selected)

    def filter_by_within_territory(self, queryset, key, value):
        territory = Territory.objects.filter(pk=value)
        if not territory.exists():
            return queryset

        return queryset.filter(
            Q(is_remote=False) & Q(venue__location__within=territory.boundaries)
        )
