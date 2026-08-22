import django_filters
from django.db import models
from .models import Car

class CarFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_filter', label='Search')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    fuel_type = django_filters.ChoiceFilter(choices=Car._meta.get_field('fuel_type').choices)
    transmission = django_filters.ChoiceFilter(choices=Car._meta.get_field('transmission').choices)
    body_type = django_filters.ChoiceFilter(choices=Car._meta.get_field('body_type').choices)

    class Meta:
        model = Car
        fields = ['q', 'min_price', 'max_price', 'fuel_type', 'transmission', 'body_type']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(make__icontains=value) |
            models.Q(model__icontains=value) |
            models.Q(year__icontains=value) |
            models.Q(description__icontains=value)
        )