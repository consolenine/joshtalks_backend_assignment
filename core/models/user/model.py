from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Ensure password is hashed before saving"""
        if self.pk is None or 'password' in self.__dict__:
            if not self.password.startswith('pbkdf2_sha256$'):  # Check if password is already hashed
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username