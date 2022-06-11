from .models import Departments
import datetime

from django.db.models.signals import post_save


def save_profile(sender, instance, **kwargs):
    instance.updated_at = datetime.datetime.now()
    instance.save()


post_save.connect(save_profile, sender=Departments)
