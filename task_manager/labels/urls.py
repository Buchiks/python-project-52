from django.urls import path

from . import views

app_name = 'labels'

urlpatterns = [
    path("", views.LabelsListView.as_view(), name="list"),
    #path("create/", , name="create"),
    #path("<int:pk>/update/", , name="update"),
    #path("<int:pk>/delete/", , name="delete"),
]