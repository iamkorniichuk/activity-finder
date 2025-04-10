from django.contrib.gis.db import models
from django.contrib.postgres.indexes import GinIndex


class Territory(models.Model):
    class Meta:
        indexes = [
            GinIndex(
                name="name_trigram_index",
                fields=("name",),
                opclasses=("gin_trgm_ops",),
            )
        ]

    class TypeChoices(models.IntegerChoices):
        COUNTRY = 0, "country"
        REGION = 1, "region"
        DISTRICT = 2, "district"
        COMMUNITY = 3, "community"
        SETTLEMENT = 4, "settlement"

    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    boundaries = models.MultiPolygonField(srid=4326, dim=2)
    upper_level = models.ForeignKey(
        "self",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="lower_levels",
    )
    type = models.PositiveSmallIntegerField(choices=TypeChoices.choices)

    def __str__(self):
        return self.name
