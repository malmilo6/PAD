from django.db import models
from django.utils import timezone


# WeatherData - Store raw weather data
class WeatherData(models.Model):
    location = models.CharField(max_length=255)
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"WeatherData from {self.location} at {self.timestamp}"


# ProcessedWeatherAlert - Alerts generated after processing weather data
class ProcessedWeatherAlert(models.Model):
    ALERT_TYPES = (
        ('storm', 'Storm'),
        ('flood', 'Flood'),
        ('heatwave', 'Heatwave'),
    )
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20)  # e.g., 'moderate', 'severe'
    description = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.alert_type.capitalize()} alert - {self.severity}"


# DataProcessingLog - Logs for data extraction and processing
class DataProcessingLog(models.Model):
    data_source = models.CharField(max_length=255)
    status = models.CharField(max_length=50)  # e.g., 'success', 'failed'
    processed_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Log for {self.data_source} - {self.status}"


# WeatherPrediction - Future weather predictions based on current trends
class WeatherPrediction(models.Model):
    location = models.CharField(max_length=255)  # e.g., 'New York'
    forecast_date = models.DateField()  # Date for the future forecast
    predicted_temperature = models.FloatField()
    predicted_wind_speed = models.FloatField()
    predicted_precipitation = models.FloatField()
    prediction_generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.location} on {self.forecast_date}"


# PredictionLog - Log of predictions made and their outcome
class PredictionLog(models.Model):
    location = models.CharField(max_length=255)
    prediction_date = models.DateField()  # Date when the prediction was made for
    actual_temperature = models.FloatField(null=True, blank=True)
    actual_wind_speed = models.FloatField(null=True, blank=True)
    actual_precipitation = models.FloatField(null=True, blank=True)
    prediction_accuracy = models.FloatField(null=True, blank=True)  # Store accuracy percentage
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction log for {self.location} on {self.prediction_date}"

class AlertPreference(models.Model):
    user_id = models.CharField(max_length=100)
    alert_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AlertPreference(user_id={self.user_id}, alert_type={self.alert_type}, location={self.location})"
