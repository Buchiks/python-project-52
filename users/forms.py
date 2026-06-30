from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError

from .models import Users


class UserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "username": _("Username")
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        help_text = _("Required. No more than 150 symbols. "
        "Only letters, digits and symbols @/./+/-/_")
        self.fields['username'].help_text = help_text


class UserUpdateForm(UserChangeForm):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Leave blank if you don't want to change it")
    )
    password_confirm = forms.CharField(
        label=_("Password conformation"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Enter the same password again")
    )

    class Meta:
        model = Users
        fields = ["first_name", "last_name", "username"]
        labels = {
            "first_name": _("Name"),
            "last_name": _("Surname"),
            "username": _("Username"),
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password or password_confirm:
            if password != password_confirm:
                raise ValidationError({
                    'password_confirm': _("Passwords do not match")
                })
            
        return cleaned_data
            
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password and not user.check_password(password):
            user.set_password(password)
        if commit:
            user.save()
  


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Username")
        self.fields['username'].widget.attrs.update({
            'aria-label': 'Имя пользователя', 
            'class': 'form-control',
        })