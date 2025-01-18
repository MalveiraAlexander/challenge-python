from django_filters import rest_framework as filters
from .models import Country

class CountryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    continent_name = filters.CharFilter(field_name='continent_name', lookup_expr='icontains')
    min_population = filters.NumberFilter(field_name='population', lookup_expr='gte')
    max_population = filters.NumberFilter(field_name='population', lookup_expr='lte')

    class Meta:
        model = Country
        fields = ['name', 'continent_name', 'min_population', 'max_population']  # Campos disponibles para filtrar