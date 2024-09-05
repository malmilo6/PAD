#!/bin/bash

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."
    while ! nc -z $SQL_HOST_WDS $SQL_PORT_WDS; do
      sleep 0.1
    done
    echo "MySQL started"
fi

# echo "Clear entire database"
# python manage.py flush --no-input

echo "Applying database migrations..."
python manage.py makemigrations 
python manage.py migrate

exec "$@"
