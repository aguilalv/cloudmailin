# Use the official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Receive deployment data as arguments and set in environment to access from the app
ARG APP_VERSION
ARG DEPLOYED_AT
ENV APP_VERSION=$APP_VERSION
ENV DEPLOYED_AT=$DEPLOYED_AT

# Set the working directory
WORKDIR /app

# Install system dependencies for common Python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application source code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE $PORT

# Start the Flask application with Gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 "cloudmailin:create_app()"

