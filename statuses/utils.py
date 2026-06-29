from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .models import Status

'''Проверяет связан ли статус с задачей'''


class StatusConnectedTestMixin(UserPassesTestMixin):

    def test_func(self):
        status = Status.objects.get(pk=self.kwargs.get("pk"))
        return not status.tasks.exists()
    
    def handle_no_permission(self):
        messages.add_message(
            self.request, 
            messages.WARNING, _("Status cannot be deleted")
            )
        return redirect('statuses:list')