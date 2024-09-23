from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from services import get_current_weather, get_weather_prediction
from backend.utils import *

class CurrentWeatherView(APIView):
    @timeout(seconds=10)
    def get(self, request, location):
        weather_data = get_current_weather(location)
        return Response({
            "location": weather_data.location,
            "weather": weather_data.weather,
            "temperature": weather_data.temperature,
            "wind_speed": weather_data.wind_speed,
        })

class WeatherPredictionView(APIView):
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
    @timeout(seconds=10)
    def get(self, request):
        return Response({"status": "healthy"}, status=200)
