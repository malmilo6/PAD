
from django.urls import path
from .views import *

urlpatterns = [
    path('current-weather/<str:location>/', CurrentWeatherView.as_view(), name='current_weather'),
    path('health_uas/', HealthCheck.as_view()),
]