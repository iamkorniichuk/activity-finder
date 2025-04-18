from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "files"

    def ready(self):
        from .signals import delete_unlinked_file as delete_unlinked_file

        return super().ready()
