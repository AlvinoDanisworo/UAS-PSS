#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to code directory
cd code

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
