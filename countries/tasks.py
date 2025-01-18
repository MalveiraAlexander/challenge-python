import requests
from celery import shared_task
from .models import Country
from django.db import transaction
from django.core.cache import cache


@shared_task
def fetch_and_store_countries():
    if cache.get('task_lock'): # Si hay una tarea en ejecución, no se ejecuta
        print("Se encuentra una tarea en ejecución")
        return "Se encuentra una tarea en ejecución"
    print("Iniciando tarea")
    cache.set('task_lock', True, timeout=3600) # Se bloquea la ejecución de la tarea por una hora
    
    url = "https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        with transaction.atomic():
            for country_data in data:
                try:
                    print(f"Procesando {country_data['name']['common']}") # Se imprime el nombre del país
                    name = f'{country_data['name']['common']} - {country_data['name']['official']}'
                    flag = country_data['flags']['svg']
                    
                    # Manejo de capital - puede ser una lista entonces se concatenan
                    capital = country_data.get('capital', [])
                    capitalToSave = ''
                    for cp in capital:
                        capitalToSave = f'{capitalToSave}, {cp}'
                    capitalToSave = capitalToSave[2:]
                    
                    population = country_data.get('population', None)
                    
                    continent = country_data.get('continents', [])
                    continent = continent[0] if continent else None
                    
                    # Manejo de zona horaria - puede ser una lista entonces se concatenan
                    timezone = country_data.get('timezones', [])
                    timezoneToSave = ''
                    for tz in timezone:
                        timezoneToSave = f'{timezoneToSave}, {tz}'
                    timezoneToSave = timezoneToSave[2:]
                    area = country_data.get('area', None)
                    
                    # Manejo de coordenadas - puede ser una lista entonces se toman los primeros dos elementos
                    latlng = country_data.get('latlng', [None, None])
                    lat, lng = latlng if len(latlng) == 2 else (None, None)

                    # Actualiza o crea el país
                    Country.objects.update_or_create(
                        name = name,
                        defaults = {
                            'flag_img': flag,
                            'capital_name': capitalToSave,
                            'population_count': population,
                            'continent_name': continent,
                            'all_timezone': timezoneToSave,
                            'area': area,
                            'latitude': lat,
                            'longitude': lng,
                        }
                    )
                except KeyError:
                    print(f"Clave faltante: {e} en {country_data.get('name', {}).get('common', 'desconocido')}") # Se imprime el error
                    continue

    except requests.RequestException as e:
        print(f"Error al obtener los datos: {e}") # Se imprime el error
        
    finally:
        print("Tarea finalizada")
        cache.delete('task_lock') # Se libera el bloqueo siempre al finalizar