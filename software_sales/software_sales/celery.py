import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "software_sales.settings")

app = Celery("software_sales")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()