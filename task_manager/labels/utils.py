from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

'''Проверяет имеет ли метка связанные с ней задачи'''


class LabelHasTasksTestMixin(UserPassesTestMixin):

    def test_func(self):
        label = self.get_object()
        return not label.tasks.exists() 

    def handle_no_permission(self):
        messages.add_message(
            self.request, 
            messages.WARNING, _("Cannot delete label")
            )
        return redirect('labels:list')