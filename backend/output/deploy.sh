```bash
# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install needed dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Command to run the application
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
```

```yaml
# .github/workflows/ci-cd.yml
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
          docker build -t myapp .

      - name: Push to Docker Hub
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker tag myapp:latest mydockerhubusername/myapp:latest
          docker push mydockerhubusername/myapp:latest

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to Production
        run: |
          ssh user@your.server.ip "
            cd /path/to/your/app &&
            docker-compose pull &&
            docker-compose up -d --build
          "
```

```text
# requirements.txt
Flask==2.0.1
unittest-xml-reporting==3.0.0
```

```bash
# Deployment Steps

1. Build the Docker image:
   ```bash
   docker build -t myapp .
   ```

2. Run the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the application at `http://localhost:5000`.

4. Push code to the main branch, which triggers the CI/CD pipeline:
   - The pipeline will run tests, build the Docker image, and deploy it to production automatically.
   - Ensure the Docker Hub credentials are stored in repository secrets as DOCKER_USERNAME and DOCKER_PASSWORD.
```

This setup ensures that your application is packaged in a Docker container, making it portable and easy to deploy across different environments. The CI/CD pipeline handles testing, building, and deploying your application automatically whenever code is pushed to the repository.