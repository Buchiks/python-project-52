from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        help_text = _("Required. No more than 150 symbols. "
        "Only letters, digits and symbols @/./+/-/_")
        self.fields['username'].help_text = help_text


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "username": _("Nickname")
            }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Username")
        