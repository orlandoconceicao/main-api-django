#!/bin/sh

echo "Aguardando banco de dados..."

# espera o Postgres ficar disponível
while ! nc -z db 5432; do
  sleep 1
done

echo "Banco de dados conectado!"

# (opcional mas recomendado) migrações automáticas
echo "Rodando migrações..."
python manage.py migrate

# (opcional) coleta arquivos estáticos
echo "Coletando static files..."
python manage.py collectstatic --noinput

echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000