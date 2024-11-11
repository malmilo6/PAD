from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from services import get_current_weather, get_weather_prediction, process_weather_data
from backend.utils import *
from circuit_breaker import circuit_breaker_decorator
import requests
from django.http import JsonResponse
from user_alert_service.middleware import RequestCounterMiddleware

import requests
from django.http import JsonResponse
from pymongo import MongoClient

# Define db connection and table in use for 2pc
MONGO_URI = "mongodb://root:mongoadmin@mongodb:27017/db_uas?authSource=admin&authMechanism=SCRAM-SHA-1"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["db_uas"]
user_preferences_collection = mongo_db["backend_alertpreference"]


class CurrentWeatherView(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request, location):
        weather_data = get_current_weather(location)
        return Response({
            "location": weather_data.location,
            "weather": weather_data.weather,
            "temperature": weather_data.temperature,
            "wind_speed": weather_data.wind_speed,
        })



class GenerateWeatherReportView(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request, location):
        current_weather = get_current_weather(location)
        forecast = get_weather_prediction(location)

        resp = process_weather_data(current_weather, forecast)
        return resp


class WeatherPredictionView(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request, location):
        weather_data = get_weather_prediction(location)
        return Response({
            "location": weather_data.location,
            "forecast_date": weather_data.forecast_date,
            "predicted_temperature": weather_data.predicted_temperature,
            "predicted_wind_speed": weather_data.predicted_wind_speed,
            "predicted_precipitation": weather_data.predicted_precipitation,
            "prediction_generated_at": weather_data.prediction_generated_at
        })


class HealthCheck(APIView):
    @circuit_breaker_decorator
    @timeout(seconds=10)
    def get(self, request):
        return Response({"status": "healthy"}, status=200)


class FailureSimulation(APIView):
    def get(self, request):
        # Randomly decide to simulate a failure
        # failure  = get_random_string(1, allowed_chars="01") == "1"
        failure = True

        if failure:
            return Response({"status": "Server Failure"}, status=500)
        else:
            return Response({"status": "No Failure"}, status=200)




def current_load(request):
    load_count = RequestCounterMiddleware.get_current_load()
    return JsonResponse({'current_load': load_count})


class CreateAlertPreference2PC(APIView):
    WDS_SERVICE_URL = "http://django-weather-data-service:8000/api/v1/alert-sync/"

    def post(self, request):
        # Extract data from the request
        user_id = request.data.get("user_id")
        alert_type = request.data.get("alert_type")
        location = request.data.get("location")

        # Prepare Phase
        try:
            # 1. Check UAS readiness by finding any potential conflicts in MongoDB
            existing_pref = user_preferences_collection.find_one({"user_id": user_id, "alert_type": alert_type})
            if existing_pref:
                return Response({"status": "failed", "message": "Alert preference already exists"},
                                status=status.HTTP_400_BAD_REQUEST)

            # 2. Call WDS prepare endpoint to verify readiness
            wds_prepare_response = requests.post(f"{self.WDS_SERVICE_URL}prepare/", json={
                "user_id": user_id, "alert_type": alert_type, "location": location
            })
            if wds_prepare_response.status_code != 200:
                raise Exception("WDS Prepare phase failed")

            print("Prepare phase successful for both services.")

        except Exception as e:
            print(f"Prepare phase failed: {e}")
            return Response({"status": f"Transaction Aborted: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Commit Phase
        try:
            # 1. Commit to MongoDB
            user_preferences_collection.insert_one({"user_id": user_id, "alert_type": alert_type, "location": location})

            # 2. Commit to WDS
            wds_commit_response = requests.post(f"{self.WDS_SERVICE_URL}commit/", json={
                "user_id": user_id, "alert_type": alert_type, "location": location
            })
            if wds_commit_response.status_code != 200:
                raise Exception("WDS Commit phase failed")

            print("Transaction committed successfully on both services.")
            return Response({"status": "Transaction Committed"}, status=status.HTTP_200_OK)

        except Exception as e:
            # Rollback
            print(f"Commit phase failed, rolling back: {e}")

            # MongoDB rollback
            user_preferences_collection.delete_one({"user_id": user_id, "alert_type": alert_type, "location": location})

            # WDS rollback
            requests.post(f"{self.WDS_SERVICE_URL}rollback/", json={
                "user_id": user_id, "alert_type": alert_type, "location": location
            })

            return Response({"status": "Transaction Rolled Back"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

