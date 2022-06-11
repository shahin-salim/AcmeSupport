from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.


class Departments(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.CharField(max_length=100, default="admin")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

