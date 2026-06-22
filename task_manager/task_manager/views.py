from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .forms import UserForm, UserUpdateForm
from .models import Users
from .utils import OwnerTestMixin


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class UsersIndexView(View):

    def get(self, request, *args, **kwargs):
        users = Users.objects.all()
        return render(
            request,
            "users_list.html",
            {"users": users}
        )


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "create_user.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users")
        
        return render(request, "create_user.html", {"form": form})

class UserUpdateView(OwnerTestMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        form = UserUpdateForm(instance=user)
        return render(request, "update_user.html", {"form" :form, "user_id": user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("User successfully updated"))
            return redirect("users")
        
        return render(request, "update_user.html", {"form" :form, "user_id": user_id})

class UserDeleteView(OwnerTestMixin, View):
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        if user:
            user.delete()
            messages.add_message(request, messages.SUCCESS, _("User successfully deleted"))
            return redirect("users")
        
class UserLoginView(View):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, _("You signed in"))
            return redirect("index")
        
        return render(request, "login.html", {"form": form})

class UserLogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, _("You signed out"))
        return redirect("index")