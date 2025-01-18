from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'megapix.settings')

app = Celery('megapix')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Detecta tareas en todos los archivos llamados tasks.py en las aplicaciones registradas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')