from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Schedule, generate_slots


@receiver(post_save, sender=Schedule)
def set_slots(sender, instance, **kwargs):
    booking_duration = instance.booking_duration
    for work_day in instance.work_days.all():
        work_hours = work_day.work_hours
        break_hours = getattr(work_day, "break_hours")
        if break_hours is None:
            break_hours = []

        work_day.slots = generate_slots(booking_duration, work_hours, break_hours)
        work_day.save(update_fields=["slots"])
