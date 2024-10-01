from datetime import datetime, timedelta
from django.http import JsonResponse

import grpc
import test_pb2_grpc as weather_service_pb2_grpc, test_pb2 as weather_service_pb2
from backend.models import WeatherReport, UserAlert


def get_current_weather(location):
    try:
        with grpc.insecure_channel('django-weather-data-service:50051') as channel:
            stub = weather_service_pb2_grpc.WeatherServiceStub(channel)
            request = weather_service_pb2.WeatherRequest(location=location)
            response = stub.GetCurrentWeather(request)
            return response
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()}, {e.details()}")
        return None


def get_weather_prediction(location):
    try:
        with grpc.insecure_channel('django-weather-data-service:50051') as channel:
            stub = weather_service_pb2_grpc.WeatherServiceStub(channel)
            request = weather_service_pb2.WeatherPredictionRequest(location=location)
            response = stub.GetWeatherPrediction(request)
            return response
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()}, {e.details()}")
        return None


def process_weather_data(current_weather, forecast):
    def fetch_current_weather(data):
        return {
            "location": data.location,
            "weather": data.weather,
            "temperature": data.temperature,
            "wind_speed": data.wind_speed
        }

    def fetch_forecast(data):
        return {
            "location": data.location,
            "forecast_date": data.forecast_date,
            "predicted_temperature": data.predicted_temperature,
            "predicted_wind_speed": data.predicted_wind_speed,
            "predicted_precipitation": data.predicted_precipitation,
            "prediction_generated_at": data.prediction_generated_at
        }
    current_weather = fetch_current_weather(current_weather)
    forecast = fetch_forecast(forecast)
    # Combine data
    combined_data = {
        "current_location": current_weather["location"],
        "current_temperature": current_weather["temperature"],
        "current_wind_speed": current_weather["wind_speed"],
        "forecast_location": forecast["location"],
        "forecast_date": forecast["forecast_date"],
        "predicted_temperature": forecast["predicted_temperature"],
        "predicted_wind_speed": forecast["predicted_wind_speed"],
        "predicted_precipitation": forecast["predicted_precipitation"],
    }

    # Create WeatherReport instance
    weather_report = WeatherReport.objects.create(
        location=current_weather["location"],
        reported_at=datetime.now(),
        temperature=current_weather["temperature"],
        wind_speed=current_weather["wind_speed"],
        precipitation=forecast["predicted_precipitation"],  # Example of using forecast data
    )

    # Create a UserAlert based on the forecast temperature
    if forecast["predicted_temperature"] > 30:  # Threshold for heatwave alert
        UserAlert.objects.create(
            user=None,  # Assign a UserProfile instance here
            alert_type='heatwave',
            description='Heatwave warning for New York',
            issued_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=6),  # Alert expires after 6 hours
            is_active=True
        )

    return JsonResponse(combined_data)
