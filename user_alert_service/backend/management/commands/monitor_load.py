# backend/management/commands/monitor_load.py
import requests
from django.core.management.base import BaseCommand
from user_alert_service.middleware import RequestCounterMiddleware
from backend.models import LoadAlert
from datetime import datetime
import time


class Command(BaseCommand):
    help = "Monitor load and create alerts based on request count."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting to monitor load...'))
        self.monitor_load()

    def monitor_load(self):
        CRITICAL_LOAD = 1  # Define your critical threshold here

        while True:
            # load_count = RequestCounterMiddleware.get_current_load()
            load_count_response = requests.get("http://localhost:8001/api/v1/current-load")
            load_count = load_count_response.json()['current_load']

            if load_count > CRITICAL_LOAD:
                LoadAlert.objects.create(
                    load_count=load_count,
                    description=f"High load detected with {load_count} requests per second at timestamp {datetime.now()}"
                )
                self.stdout.write(self.style.SUCCESS(f'Alert created: {load_count} requests detected!'))
            else:
                self.stdout.write(self.style.NOTICE(f'Current load: {load_count} requests.'))

            time.sleep(2)  # Wait a minute before checking again
