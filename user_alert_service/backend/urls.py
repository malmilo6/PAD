
from django.urls import path
from .views import *

urlpatterns = [
    path('current-weather/<str:location>/', CurrentWeatherView.as_view(), name='current_weather'),
    path('weather-prediction/<str:location>/', WeatherPredictionView.as_view(), name='weather_prediction'),
    path('health_uas/', HealthCheck.as_view()),
    path('generate-report/<str:location>', GenerateWeatherReportView.as_view(), name='generate-report')
]