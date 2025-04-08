# Generated by Django 5.1.7 on 2025-04-08 15:15

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeRange",
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
                ("start", models.TimeField()),
                ("end", models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name="WorkDay",
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
                (
                    "day",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "monday"),
                            (1, "tuesday"),
                            (2, "wednesday"),
                            (3, "thursday"),
                            (4, "friday"),
                            (5, "saturday"),
                            (6, "sunday"),
                        ]
                    ),
                ),
                (
                    "break_hours",
                    models.ManyToManyField(
                        blank=True, related_name="breaks", to="schedules.timerange"
                    ),
                ),
                (
                    "work_hours",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="works",
                        to="schedules.timerange",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
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
                (
                    "booking_duration",
                    models.DurationField(default=datetime.timedelta(seconds=3600)),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("work_days", models.ManyToManyField(to="schedules.workday")),
            ],
            options={
                "default_related_name": "schedules",
            },
        ),
    ]
