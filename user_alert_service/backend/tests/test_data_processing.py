import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_alert_service.settings')
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch

import django
django.setup()


class GenerateWeatherReportViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('generate-report', kwargs={'location': 'New York'})

    @pytest.mark.django_db
    @patch('services.get_current_weather')
    @patch('services.get_weather_prediction')
    def test_generate_weather_report(self, mock_get_weather_prediction, mock_get_current_weather):
        # Mock the responses from the weather functions
        mock_get_current_weather.return_value = {
            "location": "New York",
            "weather": "Sunny",
            "temperature": 25.0,
            "wind_speed": 15.0
        }

        mock_get_weather_prediction.return_value = {
            "location": "New York",
            "forecast_date": "2024-09-23",
            "predicted_temperature": 23.262737274169922,
            "predicted_wind_speed": 20.0,
            "predicted_precipitation": 50.0,
            "prediction_generated_at": "2024-09-22 15:37:42.835787+00:00"
        }
        # Make the GET request
        response = self.client.get(self.url)

        # Assertions for the API response
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(response_data['current_location'], 'New York')
        self.assertEqual(response_data['forecast_location'], 'New York')
        self.assertEqual(response_data['predicted_temperature'], 23.262737274169922 )

