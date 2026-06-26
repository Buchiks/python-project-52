from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path("", views.TasksListView.as_view(), name="list"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    #path("<int:pk>/update/", , name="update"),
    #path("<int:pk>/delete/", , name="delete"),
]