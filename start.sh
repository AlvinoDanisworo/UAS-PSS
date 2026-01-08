#!/bin/bash

# Start script for Railway deployment
# This script properly handles the PORT environment variable

# Debug: Check if DATABASE_URL is set
echo "=== Environment Check ==="
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is NOT set!"
    echo "Database will fallback to localhost (which will fail)"
else
    echo "DATABASE_URL is set: ${DATABASE_URL:0:30}..." # Show only first 30 chars for security
fi
echo "PORT: ${PORT}"
echo "========================="

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

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Warning: collectstatic failed"

# Setup demo data (only if database is empty)
echo "Setting up demo data..."
python manage.py setup_demo || echo "Demo data already exists or setup failed"

# Use PORT from environment or default to 8000
PORT=${PORT:-8000}

# Start gunicorn
echo "Starting gunicorn on port $PORT..."
exec gunicorn lms_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --log-level info
