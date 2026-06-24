from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path("", views.UsersIndexView.as_view(), name="index"),
    path("create/", views.UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
]