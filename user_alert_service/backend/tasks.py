# backend/tasks.py

from celery import shared_task
from django.core.cache import cache
from backend.models import LoadAlert
from datetime import datetime

def monitor_load():
    CRITICAL_LOAD = 2  # Define your critical threshold here
    current_timestamp = int(datetime.now().timestamp())
    cache_key = f"load_count_{current_timestamp}"
    load_count = cache.get(cache_key, 0)

    if load_count > CRITICAL_LOAD:
        LoadAlert.objects.create(
            load_count=load_count,
            description=f"High load detected with {load_count} requests per second at timestamp {datetime.now()}"
        )
