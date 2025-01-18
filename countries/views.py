from .models import Country
from .serializers import CountrySerializer
from .pagination import CountryPagination
from .filters import CountryFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status



# Create your views here.
class CountryViewSet(ReadOnlyModelViewSet):
    serializer_class = CountrySerializer
    pagination_class = CountryPagination
    filterset_class = CountryFilter
    search_fields = ['name', 'continent_name']
    ordering_fields = ['name', 'id', 'continent_name']
    ordering = ['name', 'id', 'continent_name']
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Country.objects.all()
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Country.DoesNotExist:
            return Response({"error": "País no encontrado"}, status=status.HTTP_404_NOT_FOUND)