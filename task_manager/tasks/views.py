from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Task
from .utils import DeleteOwnerTestMixin, OwnerTestMixin
from .filters import TaskFilter

class TasksListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        tasks_filter = TaskFilter(request.GET, queryset=tasks, request=request)
        return render(
            request,
            "task_list.html",
            {"tasks": tasks_filter}
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    
    model = Task
    fields = ["name", "executor", "status", "labels"]
    template_name = "create.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _('Task successfully created'))
        return response


class TaskUpdateView(LoginRequiredMixin, OwnerTestMixin, UpdateView):
    
    model = Task
    fields = ["name", "executor", "status", "labels"]
    template_name = "update.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Task successfully updated'))
        return response


class TaskDeleteView(LoginRequiredMixin, DeleteOwnerTestMixin, DeleteView):
    
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Task successfully deleted'))
        return response


class TaskShowView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        task_pk = kwargs.get("pk")
        task = Task.objects.get(pk=task_pk)
        return render(request, "show.html", {"task": task})