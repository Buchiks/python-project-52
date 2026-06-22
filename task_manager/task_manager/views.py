from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import UserForm, UserUpdateForm
from .models import Users


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

class UserUpdateView(View):
    
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

class UserDeleteView(View):

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        if user:
            user.delete()
            messages.add_message(request, messages.SUCCESS, _("User successfully deleted"))
            return redirect("users")