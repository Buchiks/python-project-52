from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Label


class LabelsListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(
            request,
            "labels/list.html",
            {"labels": labels}
        )
    

class LabelCreateView(LoginRequiredMixin, CreateView):
    
    model = Label
    fields = ["name"]
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully created'))
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):

    model = Label
    fields = ["name"]
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully updated'))
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):

    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        label = self.get_object()
        if label.tasks.exists():
            messages.warning(self.request, _("Cannot delete label"))
            return redirect("labels:list")
        response = super().form_valid(form)
        messages.success(self.request, _('Label successfully deleted'))
        return response
