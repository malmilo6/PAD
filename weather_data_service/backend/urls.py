from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet, HealthCheck, WeatherPredictionViewSet, AlertSync2PC

router = DefaultRouter()
router.register(r'weather-data', WeatherDataViewSet)
router.register(r'weather-prediction', WeatherPredictionViewSet)

url_patterns = [
    path('health/', HealthCheck.as_view()),
    path('', include(router.urls)),
    path('alert-sync/<str:action>/', AlertSync2PC.as_view(), name='alert_sync_2pc'),
]