#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (already in /code from WORKDIR)
python manage.py collectstatic --no-input

# Note: Don't run migrate here - Railway will do it separately or manually
