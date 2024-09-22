# from models import WeatherData
# from django_grpc_framework import proto_serializers
# from weather_data_service import test_pb2
from rest_framework import serializers, viewsets
from .models import WeatherData
from django_filters import rest_framework as filters


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'

