from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_air_erp_system.settings')

app = Celery('django_air')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
