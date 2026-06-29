from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=200, 
        unique=True, 
        error_messages={'unique': _("already exists")},
        verbose_name=_("Name")
        )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name="executor_tasks",
        verbose_name=_("Implementer")
        )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_tasks',
        verbose_name=_("Author")
        )
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT, 
        related_name='tasks',
        verbose_name=_("Status") 
        )
    labels = models.ManyToManyField(
        Label, 
        related_name='tasks',
        verbose_name=_("Label"),
        blank=True
        )
