#!/bin/bash

# Migration script for Railway
# Run this manually in Railway dashboard or CLI

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser (optional)..."
# Uncomment if you want to create superuser automatically
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Setup demo data (optional)..."
# Uncomment if you want to load demo data
# python manage.py shell < setup_demo_data.py || true

echo "Database setup complete!"
