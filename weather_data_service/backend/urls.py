from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views import WeatherDataViewSet, HealthCheck, WeatherPredictionViewSet

router = DefaultRouter()
router.register(r'weather-data', WeatherDataViewSet)
router.register(r'weather-prediction', WeatherPredictionViewSet)

url_patterns = [
    path('health_wds/', HealthCheck.as_view()),
    path('', include(router.urls))
]