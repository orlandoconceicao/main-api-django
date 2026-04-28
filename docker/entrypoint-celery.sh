#!/bin/sh

set -e

echo "Aguardando banco..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Iniciando Celery..."

exec celery -A software_sales worker -l info