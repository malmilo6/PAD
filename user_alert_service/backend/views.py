import datetime
import time

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from services import get_current_weather, get_weather_prediction, process_weather_data
from backend.utils import *
from backend.models import WeatherReport
from django.utils import timezone
from circuit_breaker import circuit_breaker_decorator

from user_alert_service.middleware import RequestCounterMiddleware


class CurrentWeatherView(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request, location):
        weather_data = get_current_weather(location)
        return Response({
            "location": weather_data.location,
            "weather": weather_data.weather,
            "temperature": weather_data.temperature,
            "wind_speed": weather_data.wind_speed,
        })


class GenerateWeatherReportView(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request, location):
        current_weather = get_current_weather(location)
        forecast = get_weather_prediction(location)

        resp = process_weather_data(current_weather, forecast)
        return resp


class WeatherPredictionView(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request, location):
        weather_data = get_weather_prediction(location)
        return Response({
            "location": weather_data.location,
            "forecast_date": weather_data.forecast_date,
            "predicted_temperature": weather_data.predicted_temperature,
            "predicted_wind_speed": weather_data.predicted_wind_speed,
            "predicted_precipitation": weather_data.predicted_precipitation,
            "prediction_generated_at": weather_data.prediction_generated_at
        })


class HealthCheck(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request):
        return Response({"status": "healthy"}, status=200)


@circuit_breaker_decorator
def failure_simulation(req):
    # Raise an exception to simulate a failure for testing.
    raise Exception("Simulated service failure")


def current_load(request):
    load_count = RequestCounterMiddleware.get_current_load()
    return JsonResponse({'current_load': load_count})