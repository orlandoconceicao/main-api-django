#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python software_sales/manage.py collectstatic --no-input
python software_sales/manage.py migrate