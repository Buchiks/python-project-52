from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Users


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["name", "surname", "nickname"]
        labels = {
            "name": _("Name"),
            "surname": _("Surname"),
            "nickname": _("Nickname")
            }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control  my-3",
                "placeholder": _("Name"),
            }),
            "surname": forms.TextInput(attrs={
                "class": "form-control  my-3",
                "placeholder": _("Surname"),
            }),
            "nickname": forms.TextInput(attrs={
                "class": "form-control my-3",
                "placeholder": _("Nickname"),
            }),
        }
