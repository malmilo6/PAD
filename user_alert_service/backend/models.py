from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    username = models.TextField(unique=True)
    is_subscribed = models.BooleanField(default=True, help_text="Is the user subscribed to receive alerts?")
    subscription_area = models.TextField()

    def __str__(self):
        return self.username


# UserAlert - Stores alerts generated for users
class UserAlert(models.Model):
    ALERT_TYPES = (
        ('storm', 'Storm'),
        ('flood', 'Flood'),
        ('heatwave', 'Heatwave'),
        ('rain', 'Rain'),
        ('normal', 'Normal')
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    description = models.TextField()
    issued_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(help_text="Time when this alert is no longer valid.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Alert: {self.alert_type.capitalize()} for {self.user.username}"


# WeatherPrediction - Handles weather predictions (future weather data)
class WeatherPrediction(models.Model):
    location = models.CharField(max_length=100)
    predicted_at = models.DateTimeField(help_text="Time when the prediction was made.")
    temperature_high = models.FloatField(help_text="Predicted high temperature.")
    temperature_low = models.FloatField(help_text="Predicted low temperature.")
    wind_speed = models.FloatField(help_text="Predicted wind speed in m/s.")
    chance_of_precipitation = models.FloatField(help_text="Chance of precipitation in percentage.")
    forecast_date = models.DateField(help_text="The date for which this prediction is made.")

    def __str__(self):
        return f"WeatherPrediction for {self.location} on {self.forecast_date}"


# 4. WeatherReport - Stores actual weather reports (historical weather data)
class WeatherReport(models.Model):
    location = models.CharField(max_length=100)
    reported_at = models.DateTimeField(help_text="Time when the report was logged.")
    temperature = models.FloatField(help_text="Actual temperature.")
    wind_speed = models.FloatField(help_text="Actual wind speed in m/s.")
    precipitation = models.FloatField(help_text="Amount of precipitation in mm.")

    def __str__(self):
        return f"WeatherReport for {self.location} at {self.reported_at}"
