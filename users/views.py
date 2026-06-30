from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomAuthenticationForm, UserForm, UserUpdateForm
from .models import Users
from .utils import OwnerTestMixin, HasTasksMixin


class UsersIndexView(View):

    def get(self, request, *args, **kwargs):
        users = Users.objects.all()
        return render(
            request,
            "users/users_list.html",
            {"users": users}
        )


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "users/create_user.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, 
                messages.SUCCESS, _("User successfully registered")
                )
            return redirect("user_login")
        
        return render(request, "users/create_user.html", {"form": form})


class UserUpdateView(OwnerTestMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        form = UserUpdateForm(instance=user)
        return render(
            request, 
            "users/update_user.html", 
            {"form": form, "user_id": user_id}
            )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, 
                messages.SUCCESS, _("User successfully updated")
                )
            return redirect("users:index")
        
        return render(
            request, 
            "users/update_user.html", 
            {"form": form, "user_id": user_id}
            )


class UserDeleteView(OwnerTestMixin, HasTasksMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        return render(
            request, 
            "users/delete_user.html", 
            {"user": user}
            )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = Users.objects.get(pk=user_id)
        if user:
            user.delete()
            messages.add_message(
                request, 
                messages.SUCCESS, _("User successfully deleted")
                )
            return redirect("users:index")
        

class UserLoginView(LoginView):

    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are already signed in"))
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, _("You signed in"))
        return reverse_lazy('index')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, _("You signed out"))
        return response