#!/bin/sh

echo "Aguardando banco de dados..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco conectado!"

echo "Iniciando Celery..."
celery -A software_sales worker -l info