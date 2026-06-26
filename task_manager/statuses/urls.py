from django.urls import path

from . import views


app_name = 'statuses'

urlpatterns = [
    path("", views.StatusesIndexView.as_view(), name="list"),
    path("create/",views.StatusesCreateView.as_view() , name="create"),
    path("<int:pk>/update/",views.StatusesUpdateView.as_view() , name="update"),
    #path("<int:pk>/delete/", , name="delete"),
]