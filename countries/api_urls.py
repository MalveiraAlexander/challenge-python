from rest_framework.routers import DefaultRouter
from .views import CountryViewSet
from django.urls import path, include

# Agrego un router ya que necesitamos agregarlo después en el archivo de urls principal
router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='countries') # Agrego la vista de los países
# Agrego r para que Python no escape los caracteres especiales y tome el field id

urlpatterns = [
    path('api/', include(router.urls)), # Agrego las URLs del router
]