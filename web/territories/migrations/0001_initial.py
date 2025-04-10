# Generated by Django 5.1.7 on 2025-04-10 19:18

import django.contrib.gis.db.models.fields
import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("commons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Territory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=12, unique=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "boundaries",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "country"),
                            (1, "region"),
                            (2, "district"),
                            (3, "community"),
                            (4, "settlement"),
                        ]
                    ),
                ),
                (
                    "upper_level",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lower_levels",
                        to="territories.territory",
                    ),
                ),
            ],
            options={
                "indexes": [
                    django.contrib.postgres.indexes.GinIndex(
                        fields=["name"],
                        name="name_trigram_index",
                        opclasses=("gin_trgm_ops",),
                    )
                ],
            },
        ),
    ]
