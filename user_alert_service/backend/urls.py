
from django.urls import path
from .views import *

urlpatterns = [
    path('current-weather/<str:location>/', CurrentWeatherView.as_view(), name='current_weather'),
    path('weather-prediction/<str:location>/', WeatherPredictionView.as_view(), name='weather_prediction'),
    path('health/', HealthCheck.as_view()),
    path('failure/', FailureSimulation.as_view(), name='failure'),
    path('generate-report/<str:location>', GenerateWeatherReportView.as_view(), name='generate-report'),
    path('current-load/', current_load, name='current_load'),
    path('user-alert-preference/', CreateAlertPreference2PC.as_view(), name='user-alert-preference'),
]