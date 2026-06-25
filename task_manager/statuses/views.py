from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from .models import Status
from .forms import StatusForm

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
            return redirect("statuses:list")
        
        return render(request, "status_create.html", {"form": form})