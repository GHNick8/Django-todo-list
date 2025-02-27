# Step 1: Use an official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run database migrations
RUN python manage.py migrate --noinput

# Collect static files (if using Django's static files)
RUN python manage.py collectstatic --noinput

# Expose the port Railway assigns
EXPOSE 8080

# Start the Django application using Gunicorn
CMD ["gunicorn", "todo_project.wsgi:application", "--bind", "0.0.0.0:8080"]


