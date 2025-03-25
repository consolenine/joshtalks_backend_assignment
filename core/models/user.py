# core/models/user.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)

    class Roles(models.TextChoices):
        MANAGER = 'manager', _('Manager')
        EMPLOYEE = 'employee', _('Employee')

    role = models.CharField(max_length=10, choices=Roles, default=Roles.EMPLOYEE)

    def __str__(self):
        return self.username