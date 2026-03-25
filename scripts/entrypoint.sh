#!/usr/bin/env bash
python manage.py migrate
python manage.py runserver ${LISTEN:-0.0.0.0}:${PORT:8567}
