#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (already in /code from WORKDIR)
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
