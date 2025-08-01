# Generated by Django 5.1.7 on 2025-04-19 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("activities", "0002_activity_media_delete_activitymedia"),
        ("venues", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="activity",
            name="location",
        ),
        migrations.AddField(
            model_name="activity",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="venues.venue",
            ),
        ),
    ]
