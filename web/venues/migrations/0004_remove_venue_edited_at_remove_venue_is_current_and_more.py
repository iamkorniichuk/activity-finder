# Generated by Django 5.1.7 on 2025-05-18 11:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("venues", "0003_venue_is_current"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="venue",
            name="edited_at",
        ),
        migrations.RemoveField(
            model_name="venue",
            name="is_current",
        ),
        migrations.RemoveField(
            model_name="venue",
            name="previous_version",
        ),
    ]
