from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DeleteView

from .forms import StatusForm
from .models import Status


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


class StatusesDeleteView(LoginRequiredMixin, DeleteView):

    model = Status
    template_name = "status_delete.html"
    success_url = reverse_lazy("statuses:list")
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, _("Status successfully deleted"))
            return response
        except ProtectedError:
            messages.warning(self.request, _("Status cannot be deleted"))
            return redirect("statuses:list")