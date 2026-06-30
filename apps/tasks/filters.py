import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.labels.models import Label

from .models import Task


class TaskFilter(django_filters.FilterSet):
    my_tasks = django_filters.BooleanFilter(
        method="filter_my_tasks",
        label=_("Only your tasks"),
        widget=forms.CheckboxInput
    )
    label = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all().order_by('name'),
        lookup_expr='exact',
        label=_("Label"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Task
        fields = ["status", "executor", "label", "my_tasks"]
    
    def filter_my_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset