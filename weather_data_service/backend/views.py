from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import *
from backend.serializers import *
from backend.utils import *
import time


class HealthCheck(APIView):
    @timeout(seconds=5)
    def get(self, request):
        # time.sleep(10) # Test time out
        return Response({"status": "healthy"}, status=200)


class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

    @timeout(seconds=10)
    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

    @timeout(seconds=10)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response

    @timeout(seconds=10)
    def delete(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return response


class WeatherPredictionViewSet(viewsets.ModelViewSet):
    queryset = WeatherPrediction.objects.all()
    serializer_class = WeatherPredictionSerializer

    @timeout(seconds=10)
    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

    @timeout(seconds=10)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response

    @timeout(seconds=10)
    def delete(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return response
