from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views import View

from .models import Task
from .utils import OwnerTestMixin, DeleteOwnerTestMixin

class TasksListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(
            request,
            "task_list.html",
            {"tasks": tasks}
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    
    model = Task
    fields = ["name", "executor", "status"]
    template_name = "create.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerTestMixin, UpdateView):
    
    model = Task
    fields = ["name", "executor", "status"]
    template_name = "update.html"
    success_url = reverse_lazy("tasks:list")


class TaskDeleteView(LoginRequiredMixin, DeleteOwnerTestMixin, DeleteView):
    
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy("tasks:list")

class TaskShowView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        task_pk = kwargs.get("pk")
        task = Task.objects.get(pk=task_pk)
        return render(request, "show.html", {"task": task})