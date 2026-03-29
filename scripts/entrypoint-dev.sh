#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input --username=${SUPERUSER:-root} --email=${SUPERUSER_EMAIL:-none@example.com}
python manage.py livereload &
python manage.py runserver ${LISTEN:-0.0.0.0}:${PORT:-8567}
