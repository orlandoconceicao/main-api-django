#!/bin/sh

echo "⏳ Aguardando banco de dados..."

# espera o Postgres ficar disponível
while ! nc -z db 5432; do
  sleep 1
done

echo "Banco conectado!"

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Iniciando Django (DEV mode)..."
python manage.py runserver 0.0.0.0:8000