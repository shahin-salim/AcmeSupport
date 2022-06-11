from .models import Departments
import datetime

from django.db.models.signals import post_save

# update last update date in department model using signal
def update_last_update_date(sender, instance, **kwargs):
    instance.updated_at = datetime.datetime.now()
    instance.save()


post_save.connect(update_last_update_date, sender=Departments)
