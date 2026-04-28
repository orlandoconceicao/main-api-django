#!/bin/sh

echo "Aguardando banco de dados..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco conectado!"

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."

exec gunicorn software_sales.wsgi:application --bind 0.0.0.0:8000