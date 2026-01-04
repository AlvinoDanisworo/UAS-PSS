#!/bin/bash

# Start script for Railway deployment
# This script properly handles the PORT environment variable

# Use PORT from environment or default to 8000
PORT=${PORT:-8000}

# Start gunicorn
exec gunicorn lms_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --log-level info
