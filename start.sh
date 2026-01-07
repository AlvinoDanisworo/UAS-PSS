#!/bin/bash

# Start script for Railway deployment
# This script properly handles the PORT environment variable

# Run migrations first (with retry logic)
echo "Running database migrations..."
max_retries=5
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if python manage.py migrate --noinput; then
        echo "Migrations completed successfully!"
        break
    else
        retry_count=$((retry_count + 1))
        echo "Migration attempt $retry_count failed. Retrying in 3 seconds..."
        sleep 3
    fi
done

if [ $retry_count -eq $max_retries ]; then
    echo "Warning: Migrations failed after $max_retries attempts. Starting anyway..."
fi

# Use PORT from environment or default to 8000
PORT=${PORT:-8000}

# Start gunicorn
echo "Starting gunicorn on port $PORT..."
exec gunicorn lms_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --log-level info
