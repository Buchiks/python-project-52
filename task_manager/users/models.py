from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ["id"]