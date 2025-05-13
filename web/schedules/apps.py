from django.apps import AppConfig


class SchedulesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "schedules"

    def ready(self):
        from .signals import set_slots as set_slots

        return super().ready()
