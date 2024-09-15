"""
Database user Model.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'