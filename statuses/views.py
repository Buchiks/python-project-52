from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import StatusForm
from .models import Status
from .utils import StatusConnectedTestMixin


class StatusesIndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, "statuses_list.html", {"statuses": statuses})


class StatusesCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, "status_create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, 
                messages.SUCCESS, 
                _("Status successfully created")
                )
            return redirect("statuses:list")
        
        return render(request, "status_create.html", {"form": form})


class StatusesUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = Status.objects.get(pk=status_id)
        form = StatusForm(instance=status)
        return render(request, "status_update.html", {
            "form": form, 
            "status_id": status_id
            }
            )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = Status.objects.get(pk=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, 
                messages.SUCCESS, 
                _("Status successfully updated")
                )
            return redirect("statuses:list")
        
        return render(request, "status_update.html", {
            "form": form, 
            "status_id": status_id
            }
            )


class StatusesDeleteView(StatusConnectedTestMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = Status.objects.get(pk=status_id)
        return render(
            request, 
            "status_delete.html", 
            {"status": status}
            )
    
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = Status.objects.get(pk=status_id)
        if status:
            status.delete()
            messages.add_message(
                request, 
                messages.SUCCESS, 
                _("Status successfully deleted")
                )
            return redirect("statuses:list")