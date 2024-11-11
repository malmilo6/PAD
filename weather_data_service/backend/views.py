from .serializers import *
from backend.utils import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import WeatherPredictionSerializer
from .models import *

class HealthCheck(APIView):
    @timeout(seconds=5)
    def get(self, request):
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


class AlertSync2PC(APIView):

    def post(self, request, action):
        user_id = request.data.get("user_id")
        alert_type = request.data.get("alert_type")
        location = request.data.get("location")

        # Handle actions based on the URL endpoint (prepare, commit, rollback)
        if action == "prepare":
            return self.prepare(user_id, alert_type)
        elif action == "commit":
            return self.commit(user_id, alert_type, location)
        elif action == "rollback":
            return self.rollback(user_id, alert_type, location)
        else:
            return Response({"status": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    def prepare(self, user_id, alert_type):
        # Prepare Phase: Check for existing alert preference in WDS (dry-run check)
        if AlertPreference.objects.filter(user_id=user_id, alert_type=alert_type).exists():
            return Response({"status": "failed", "message": "Alert preference already exists in WDS"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "prepared"}, status=status.HTTP_200_OK)

    @transaction.atomic
    def commit(self, user_id, alert_type, location):
        # Commit Phase: Insert the alert preference in WDS
        try:
            AlertPreference.objects.create(user_id=user_id, alert_type=alert_type, location=location)
            return Response({"status": "committed"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Commit failed in WDS: {e}")
            return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def rollback(self, user_id, alert_type, location):
        # Rollback Phase: Remove the alert preference if it was created
        AlertPreference.objects.filter(user_id=user_id, alert_type=alert_type, location=location).delete()
        return Response({"status": "rolled_back"}, status=status.HTTP_200_OK)
