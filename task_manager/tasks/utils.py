from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from .models import Task

'''Проверяет является ли пользователь владельцем или админом'''


class OwnerTestMixin(UserPassesTestMixin):

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs.get("pk"))
        return self.request.user == task.author or self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.add_message(
            self.request, 
            messages.WARNING, _("You don't have permission")
            )
        return redirect('tasks:list')
    
class DeleteOwnerTestMixin(OwnerTestMixin):
    def handle_no_permission(self):
        messages.add_message(
            self.request, 
            messages.WARNING, _("Task can only be deleted by it's author")
            )
        return redirect('tasks:list')
