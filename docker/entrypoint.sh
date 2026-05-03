#!/bin/sh

echo "Esperando banco..."
sleep 5

echo "Rodando migrate..."
python manage.py migrate --noinput

echo "Rodando collectstatic..."
python manage.py collectstatic --noinput

echo "Iniciando servidor..."

gunicorn core.wsgi:application --bind 0.0.0.0:$PORT