#!/bin/sh

set -e

echo "Aguardando banco..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Coletando static..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."

exec gunicorn software_sales.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 3 \
  --timeout 120