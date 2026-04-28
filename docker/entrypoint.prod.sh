#!/bin/sh

echo "Aguardando banco de dados..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco de dados conectado!"

echo "Rodando migrações..."
python manage.py migrate --noinput

echo "Coletando static files..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn (PROD)..."
gunicorn software_sales.wsgi:application --bind 0.0.0.0:8000 --workers 3