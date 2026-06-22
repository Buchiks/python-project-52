from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Users


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "username": _("Nickname")
            }
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control  my-3",
                "placeholder": _("Name"),
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control  my-3",
                "placeholder": _("Surname"),
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control my-3",
                "placeholder": _("Nickname"),
            }),
        }
