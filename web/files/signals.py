from functools import lru_cache
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.apps import apps

from .models import File


@lru_cache
def get_file_relations():
    result = []
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if field.many_to_many and getattr(field, "related_model", None) == File:
                result.append((model, field.name))
    return result


def delete_unused_file(file):
    for model, field_name in get_file_relations():
        lookup = {field_name: file}
        references = model.objects.filter(**lookup)
        if references.exists():
            return

    file.delete()


@receiver(m2m_changed)
def delete_unlinked_file(sender, instance, action, model, pk_set, **kwargs):
    if action != "post_remove" or model != File:
        return

    for pk in pk_set:
        try:
            file = File.objects.get(pk=pk)
            delete_unused_file(file)
        except File.DoesNotExist:
            pass
