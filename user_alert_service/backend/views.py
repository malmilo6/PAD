from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from services import get_current_weather
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


class HealthCheck(APIView):
    @timeout(seconds=10)
    def get(self, request):
        return Response({"status": "healthy"}, status=200)
