import random

from django.http import JsonResponse
from django.template.defaultfilters import random
from rest_framework.views import APIView
from rest_framework.response import Response
from services import get_current_weather, get_weather_prediction, process_weather_data
from backend.utils import *
from circuit_breaker import circuit_breaker_decorator
from django.utils.crypto import get_random_string


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


class FailureSimulation(APIView):
    def get(self, request):
        # Randomly decide to simulate a failure
        failure  = get_random_string(1, allowed_chars="01") == "1"

        if failure:
            return Response({"status": "Server Failure"}, status=500)
        else:
            return Response({"status": "No Failure"}, status=200)




def current_load(request):
    load_count = RequestCounterMiddleware.get_current_load()
    return JsonResponse({'current_load': load_count})