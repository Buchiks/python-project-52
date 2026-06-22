from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


'''Проверяет является ли пользователь владельцем или админом'''
class OwnerTestMixin(UserPassesTestMixin):

    def test_func(self):
        user_id = self.kwargs.get("pk")
        return self.request.user.id == user_id or self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.add_message(self.request, messages.WARNING, _("You don't have permission"))
        return redirect('users')