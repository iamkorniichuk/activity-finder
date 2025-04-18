from django.db import models


class File(models.Model):
    class Meta:
        ordering = ["order"]

    file = models.FileField()
    order = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def __repr__(self):
        return f"File({self.file.name})"
