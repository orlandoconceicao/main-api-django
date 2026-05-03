#!/bin/sh

echo "Iniciando..."

sleep 5

echo "Migrando..."
python manage.py migrate --noinput

echo "Static..."
python manage.py collectstatic --noinput

echo "Run server..."

gunicorn software_sales.core.wsgi:application --bind 0.0.0.0:$PORT