#!/bin/bash

# Check if MongoDB is up and running on the specified host and port
echo "Waiting for MongoDB at $MONGO_HOST..."
while ! nc -z $MONGO_HOST $MONGO_PORT; do
  sleep 1
done
echo "MongoDB started"

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

exec "$@"