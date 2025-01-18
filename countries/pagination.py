from rest_framework.pagination import PageNumberPagination

class CountryPagination(PageNumberPagination):
    page_size = 10  # Tamaño de la página por defecto
    page_size_query_param = 'page_size'  # Permite cambiar el tamaño de la página