# Task Management Application

## Description
This project is a task management system built with Django and Django Rest Framework. It allows users to create, assign, and manage tasks with different statuses and types.

## Create .env file

Copy .env.example file to .env and update the values as needed.

## Docker Setup Instructions

1. **Install Docker**: Make sure you have Docker installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).

2. **Build Docker Image**:
    ```sh
    docker compose up -d --build
    ```
   
3**Create Superuser**:
    ```sh
    docker exec -it <container_id> python manage.py createsuperuser
    ```

4**Access the Application**: Open your browser and go to `http://localhost:8000`.