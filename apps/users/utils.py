from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from .models import Users

'''Проверяет является ли пользователь владельцем или админом'''


class OwnerTestMixin(UserPassesTestMixin):

    def test_func(self):
        user_id = self.kwargs.get("pk")
        return self.request.user.id == user_id or self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.add_message(
            self.request, 
            messages.WARNING, _("You don't have permission")
            )
        return redirect('users:index')


class HasTasksMixin:
    def dispatch(self, request, *args, **kwargs):
        user = Users.objects.get(pk=self.kwargs.get("pk"))
        if user.executor_tasks.exists():
            messages.warning(request, _("Cannot be deleted. User has tasks"))
            return redirect('users:index')
        return super().dispatch(request, *args, **kwargs)