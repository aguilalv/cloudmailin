# Use the official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

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

### OLD ###

# Use an official lightweight Python image.
#FROM python:3.12-slim

# Copy local code to the container image.
#WORKDIR /app
#COPY main.py .
#COPY requirements.txt .

# Install dependencies into this container so there's no need to 
# install anything at container run time.
#RUN pip install -r requirements.txt

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
#ENV PORT 8080

# Run the web service on container startup. Here you use the gunicorn
# server, with one worker process and 8 threads. For environments 
# with multiple CPU cores, increase the number of workers to match 
# the number of cores available.
#CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app

