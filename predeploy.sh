#!/bin/bash

# Pre-deploy script - runs migrations before starting the app
echo "Running database migrations..."
python manage.py migrate --noinput

echo "Migrations completed successfully!"
