```bash
#!/bin/bash

# deployment.sh - Script for deploying the student planner application

echo "Starting deployment process..."

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t student-planner:latest .

# Step 2: Run migrations and collect static files
echo "Running application setup..."
docker run --rm student-planner:latest python manage.py migrate
docker run --rm student-planner:latest python manage.py collectstatic --noinput

# Step 3: Start the application
echo "Starting application services..."
docker-compose up -d

echo "Deployment completed successfully!"
```

```yaml
# docker-compose.yml - Docker Compose configuration for the student planner application

version: '3.8'

services:
  web:
    image: student-planner:latest
    build: .
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://user:password@db:5432/student_planner
      - SECRET_KEY=your_secret_key
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: student_planner
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

```dockerfile
# Dockerfile - Docker configuration for the student planner application

FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```yaml
# ci-cd-pipeline.yml - CI/CD pipeline configuration using GitHub Actions

name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m unittest discover -s tests

      - name: Build Docker image
        run: |
          docker build -t student-planner:latest .

      - name: Push Docker image to Docker Hub
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
        run: |
          echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
          docker tag student-planner:latest $DOCKER_USERNAME/student-planner:latest
          docker push $DOCKER_USERNAME/student-planner:latest

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to Production
        run: |
          ssh user@yourserver "bash /path/to/deployment.sh"
```

```text
# README.md - Documentation for the deployment process

# Student Planner Application Deployment

## Requirements
- Docker
- Docker Compose
- A suitable server with SSH access for deployment

## Deployment Steps
1. Create a `.env` file and specify your environment variables (e.g., database credentials, secret key).
2. Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. For CI/CD, set up GitHub Actions with the `ci-cd-pipeline.yml` file:
   - Ensure you have your Docker username and password stored as secrets in your GitHub repository.
4. To deploy the application, run the `deployment.sh` script on your target server, which handles Docker image builds and starting services.

This README serves as a guide for users looking to deploy and maintain the Student Planner Application effectively.
```