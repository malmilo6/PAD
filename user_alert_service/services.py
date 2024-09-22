import grpc
import test_pb2_grpc as weather_service_pb2_grpc, test_pb2 as weather_service_pb2

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