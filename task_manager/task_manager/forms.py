from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Users


class UserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "username": _("Nickname")
            }
