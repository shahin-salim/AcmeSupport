from urllib import request
from django.db import models
from django.core import validators
from department.models import Departments
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password

# user model


class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        _('email address'), unique=True, blank=True, null=True)

    phone_number_regex = RegexValidator(
        regex=r'^[789]\d{9}$', message="Enter a valid phone phone number")
    phone_number = models.CharField(
        validators=[phone_number_regex], unique=True, max_length=10,  blank=True, null=True)

    password = models.CharField(
        max_length=200, null=True, validators=[validate_password])

    department_fk = models.ForeignKey(Departments, on_delete=models.CASCADE)
    role = models.CharField(default="user", max_length=20)
    created_by = models.CharField(max_length=200, default="admin")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

