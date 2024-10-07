# backend/tasks.py

from celery import shared_task
from django.core.cache import cache
from backend.models import LoadAlert
from datetime import datetime


@shared_task
def monitor_load():
    CRITICAL_LOAD = 60  # Define your critical threshold here

    # Get the current timestamp (rounded to the second)
    current_timestamp = int(datetime.now().timestamp())

    # Retrieve the request count for the current second
    cache_key = f"load_count_{current_timestamp}"
    load_count = cache.get(cache_key, 0)

    if load_count > CRITICAL_LOAD:
        # Raise an alert - log in the database
        LoadAlert.objects.create(
            load_count=load_count,
            description=f"High load detected with {load_count} requests per second at timestamp {datetime.now()}"
        )
