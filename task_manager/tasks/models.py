from django.db import models
from django.conf import settings

from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=200, unique=True)
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="executor_tasks")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tasks' )
