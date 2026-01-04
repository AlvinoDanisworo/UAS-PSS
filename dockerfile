FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY code/ /code/

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Copy start script
COPY start.sh /code/
RUN chmod +x /code/start.sh

# Expose port
EXPOSE 8000

# Run start script
CMD ["/code/start.sh"]
