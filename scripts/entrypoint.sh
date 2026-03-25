#!/usr/bin/env bash
python manage.py migrate
python manage.py createsuperuser --no-input --username=${SUPERUSER:-root} --email=${SUPERUSER_EMAIL:-none@example.com}
python manage.py runserver ${LISTEN:-0.0.0.0}:${PORT:-8567}
