import os

from django.apps import AppConfig
import requests
import logging

from django.core.management import call_command

logger = logging.getLogger(__name__)

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        super().ready()
        # Ping another service when the app starts
        self.ping_service()

    def ping_service(self):
        service_url = 'http://service_discovery:5000/register'
        payload = {
            'name': 'django-weather-data-service',
            'ip': '127.0.0.1',
            'port': '8000',
        }

        try:
            response = requests.post(service_url, json=payload)
            if response.status_code == 200:
                logger.info('Successfully pinged the service discovery server.')
            else:
                logger.error(f'Failed to ping the service discovery server. Status code: {response.status_code}')
        except requests.RequestException as e:
            logger.error(f'Error pinging the service discovery server: {e}')