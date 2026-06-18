from django.shortcuts import redirect, render
from django.views import View

from .forms import UserForm
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