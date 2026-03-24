#!/bin/bash

# Django setup script for little_wms container
# This script runs database migrations and creates a superuser

echo "Running Django migrations..."
sudo docker exec -it little_wms-web-1 python manage.py migrate

echo "Creating Django superuser..."
sudo docker exec -it little_wms-web-1 python manage.py createsuperuser

echo "Setup complete!"
