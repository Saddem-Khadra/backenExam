from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    alias = models.CharField(max_length=200, null=False, blank=False)
    dateOfBirth = models.DateField(null=False, blank=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    objects = CustomUserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'alias', 'dateOfBirth']

    def __str__(self):
        return str(self.email)
