from django.core.management.base import BaseCommand
from backend.models import WeatherData, ProcessedWeatherAlert, DataProcessingLog, WeatherPrediction, PredictionLog
import random
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generate dummy weather data'

    def handle(self, *args, **kwargs):
        # Generate dummy WeatherData
        locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        for location in locations:
            for _ in range(10):  # Generate 10 entries per location
                weather_data = WeatherData.objects.create(
                    location=location,
                    temperature=random.uniform(-10, 40),
                    wind_speed=random.uniform(0, 20),
                    precipitation=random.uniform(0, 100)
                )
                self.stdout.write(f'Created {weather_data}')

        alert_types = ['storm', 'flood', 'heatwave']
        for _ in range(5):  # Generate 5 alerts
            alert = ProcessedWeatherAlert.objects.create(
                alert_type=random.choice(alert_types),
                severity=random.choice(['moderate', 'severe']),
                description='This is a dummy alert.',
                location=random.choice(locations)
            )
            self.stdout.write(f'Created {alert}')

        # Generate dummy DataProcessingLog
        for _ in range(5):
            log = DataProcessingLog.objects.create(
                data_source='Weather API',
                status=random.choice(['success', 'failed']),
                message='This is a dummy log message.'
            )
            self.stdout.write(f'Created {log}')

        # Generate dummy WeatherPrediction
        for location in locations:
            for days in range(1, 6):  # Generate predictions for the next 5 days
                forecast_date = timezone.now().date() + timedelta(days=days)
                prediction = WeatherPrediction.objects.create(
                    location=location,
                    forecast_date=forecast_date,
                    predicted_temperature=random.uniform(-10, 40),
                    predicted_wind_speed=random.uniform(0, 20),
                    predicted_precipitation=random.uniform(0, 100)
                )
                self.stdout.write(f'Created {prediction}')

        # Generate dummy PredictionLog
        for location in locations:
            for days in range(1, 6):
                prediction_date = timezone.now().date() + timedelta(days=days)
                prediction_log = PredictionLog.objects.create(
                    location=location,
                    prediction_date=prediction_date,
                    actual_temperature=random.uniform(-10, 40),
                    actual_wind_speed=random.uniform(0, 20),
                    actual_precipitation=random.uniform(0, 100),
                    prediction_accuracy=random.uniform(70, 100)  # Random accuracy between 70% and 100%
                )
                self.stdout.write(f'Created {prediction_log}')

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data!'))
