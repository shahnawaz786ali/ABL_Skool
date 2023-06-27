import django_filters
from django import forms

from .models import Standard,Lesson,Subject

class ClassFilter(django_filters.FilterSet):

    category = django_filters.ModelChoiceFilter(
        queryset=Standard.objects.all(),
        empty_label="All Categories",
        label="Categories",
        widget=forms.Select(attrs={'class': 'form-control'}),
        )

    class Meta:
        model = Standard
        fields = ["__all__"]