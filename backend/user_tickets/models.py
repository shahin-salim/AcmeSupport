from django.db import models

from accounts.models import CustomUser
# Create your models here.


# save user id with the request id of zendesk
class UserWithRequestId(models.Model):
    request_id = models.CharField(max_length=200, unique=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
