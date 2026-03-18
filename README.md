# Smart Vehicle Maintenance Tracker

A full-stack web application built with Django to manage vehicles, track maintenance, and monitor costs.

## Features
-   **Vehicle Management**: Add and manage multiple vehicles.
-   **Maintenance Logging**: Track services, oil changes, and tire replacements.
-   **Analytics Dashboard**: Visualize maintenance costs over time with Chart.js.
-   **Health Score**: Monitor your vehicle's maintenance health.
-   **Smart Alerts**: Get notified about upcoming and overdue services.

## Tech Stack
-   **Backend**: Django (Python)
-   **Frontend**: Bootstrap 5, Chart.js
-   **Static Files**: WhiteNoise
-   **Deployment**: Render (Ready)

## Getting Started

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```
3.  **Start the server**:
    ```bash
    python manage.py runserver
    ```

## Deployment on Render
1.  Connect your GitHub repository to Render.
2.  Select **Web Service**.
3.  Use the following settings:
    -   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    -   **Start Command**: `gunicorn vehicle_tracker.wsgi`
    -   **Environment Variables**:
        -   `DEBUG`: `False`
        -   `SECRET_KEY`: `your-secret-key`
        -   `DATABASE_URL`: `your-postgres-url`
