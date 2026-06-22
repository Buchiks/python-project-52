from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=200, blank=True)
    surname = models.CharField(max_length=200, blank=True)
    nickname = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]