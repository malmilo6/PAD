from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views import WeatherDataViewSet, HealthCheck

router = DefaultRouter()
router.register(r'weatherData', WeatherDataViewSet)

url_patterns = [
    path('health_wds/', HealthCheck.as_view()),
    path('', include(router.urls))
]