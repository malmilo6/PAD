# Generated by Django 3.0 on 2024-09-21 19:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataProcessingLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_source', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('processed_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PredictionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('prediction_date', models.DateField()),
                ('actual_temperature', models.FloatField(blank=True, null=True)),
                ('actual_wind_speed', models.FloatField(blank=True, null=True)),
                ('actual_precipitation', models.FloatField(blank=True, null=True)),
                ('prediction_accuracy', models.FloatField(blank=True, null=True)),
                ('logged_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedWeatherAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_type', models.CharField(choices=[('storm', 'Storm'), ('flood', 'Flood'), ('heatwave', 'Heatwave')], max_length=50)),
                ('severity', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('triggered_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('temperature', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('precipitation', models.FloatField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('forecast_date', models.DateField()),
                ('predicted_temperature', models.FloatField()),
                ('predicted_wind_speed', models.FloatField()),
                ('predicted_precipitation', models.FloatField()),
                ('prediction_generated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]