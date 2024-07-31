from __future__ import unicode_literals # absolute_import 
import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialme.settings')

app = Celery('socialme')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"
