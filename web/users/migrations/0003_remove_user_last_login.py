# Generated by Django 5.1.7 on 2025-04-07 06:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_birth_date_user_description_user_display_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="last_login",
        ),
    ]
