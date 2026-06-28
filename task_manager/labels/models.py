from django.db import models
from django.utils.translation import gettext_lazy as _

from tasks.models import Task


class Labels(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tasks = models.ManyToManyField(
        Task, 
        related_name='labels',
        verbose_name=_("Tasks"),
        blank=True
        )
    def __str__(self):
        return self.name