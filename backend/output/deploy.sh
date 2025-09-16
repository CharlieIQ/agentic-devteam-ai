```bash
# Dockerfile for Mini ERP System Application
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application source code
COPY . /app

# Install required packages
RUN pip install Flask Flask-Cors

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
```

```dockerfile
# Dockerfile for React front-end
FROM node:14

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install front-end dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the production assets
RUN npm run build

# Install serve to serve the static files
RUN npm install -g serve

# Command to serve the application
CMD ["serve", "-s", "build"]
```

```yaml
# docker-compose.yml
version: '3.7'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - ENV=production

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

```bash
# deployment.sh - Deployment script for production
#!/bin/bash

# Set variables
PROJECT_DIR="/path/to/your/project"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"

# Change to project directory
cd $PROJECT_DIR

# Pull the latest images
docker-compose pull

# Stop running containers and remove them if they exist
docker-compose down

# Build and start the containers
docker-compose up -d --build

# Display logs
docker-compose logs -f
```

```yaml
# .github/workflows/ci-cd-pipeline.yml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: pip install -r backend/requirements.txt

    - name: Run Tests
      run: python -m unittest discover -s backend/tests

    - name: Build Frontend
      run: |
        cd frontend
        npm install
        npm run build

    - name: Build and Push Docker Images
      run: |
        docker build -t your-docker-user/backend:latest ./backend
        docker build -t your-docker-user/frontend:latest ./frontend
        echo "$DOCKER_PASSWORD" | docker login --username your-docker-user --password-stdin
        docker push your-docker-user/backend:latest
        docker push your-docker-user/frontend:latest

    - name: Deploy to Production
      run: |
        ssh user@your-server "cd /path/to/your/project && git pull && ./deployment.sh"
```

```shell
# Instructions to set up production environment
1. Ensure Docker and Docker Compose are installed on the server.
2. Clone the repository to server:
   git clone https://github.com/your-repo.git
   cd your-repo

3. Create a .env file for the environment variables (if needed).

4. Build and deploy using docker-compose:
   docker-compose up -d --build

5. Access the application through the exposed ports (e.g., http://your-server-ip:3000 for frontend).
```

The deployment script and configuration files above will set up the application with Docker, ensuring a smooth production deployment process. The CI/CD pipeline is configured to run tests, build images, push to Docker Hub, and automatically deploy updates when new code is pushed to the main branch.