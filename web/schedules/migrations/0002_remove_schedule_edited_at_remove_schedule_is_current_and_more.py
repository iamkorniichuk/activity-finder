# Generated by Django 5.1.7 on 2025-05-18 11:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("schedules", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schedule",
            name="edited_at",
        ),
        migrations.RemoveField(
            model_name="schedule",
            name="is_current",
        ),
        migrations.RemoveField(
            model_name="schedule",
            name="previous_version",
        ),
    ]
