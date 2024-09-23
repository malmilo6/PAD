from http.client import responses

import grpc
from concurrent import futures
import test_pb2_grpc as weather_service_pb2_grpc, test_pb2 as weather_service_pb2
from backend.models import WeatherData, WeatherPrediction


class WeatherService(weather_service_pb2_grpc.WeatherServiceServicer):
    def GetCurrentWeather(self, request, context):
        location = request.location
        # Simulated data. Replace this with actual weather data retrieval logic.
        weather_data_obj = WeatherData.objects.filter(location=location).first()
        response = weather_service_pb2.WeatherResponse(
            location=weather_data_obj.location,
            weather="Sunny",
            temperature=weather_data_obj.temperature,
            wind_speed=weather_data_obj.wind_speed
        )
        return response

    def GetWeatherPrediction(self, request, context):
        location = request.location
        weather_data_obj = WeatherPrediction.objects.filter(location=location).first()

        if weather_data_obj is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"No weather prediction found for location: {location}")
            return weather_service_pb2.WeatherPredictionResponse()

        response = weather_service_pb2.WeatherPredictionResponse(
            location=weather_data_obj.location,
            forecast_date=str(weather_data_obj.forecast_date),
            predicted_temperature=weather_data_obj.predicted_temperature,
            predicted_wind_speed=weather_data_obj.predicted_wind_speed,
            predicted_precipitation=weather_data_obj.predicted_precipitation,
            prediction_generated_at=str(weather_data_obj.prediction_generated_at)
        )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_service_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC WeatherService running on port 50051...")
    server.wait_for_termination()