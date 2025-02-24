# webpush-py

English | [日本語](README_ja.md)

## Project Overview

This project demonstrates how to implement push notifications using Python and FastAPI. It allows users to easily experience push notifications by following a few simple steps. The project includes a web interface where users can subscribe to push notifications and receive them in real-time.

## Features

- Easy setup and configuration
- Uses Docker for containerization
- Generates self-signed SSL certificates for secure communication
- Registers a service worker to handle push notifications
- Allows users to subscribe and unsubscribe from push notifications
- Sends push notifications using a simple script

## How to Experience Push Notifications

1. Clone the repository:
    ```bash
    git clone https://github.com/tom96da/webpush-py.git
    cd webpush-py
    ```

2. Generate server certificates for nginx and build the Docker containers:
    ```bash
    source build.sh
    ```

3. Import the server certificate into your browser to avoid SSL warnings. The certificate is located at `nginx/ssl/server.crt`.

4. Access the home page from your browser and enable push notifications:
    - Open your browser and navigate to `https://localhost`.
    - Check the "Push Notifications" checkbox to subscribe.
    - Note: The service worker will be registered when you access the page. Ensure that the server's self-signed certificate is trusted by your browser.

5. Publish a notification and verify that the browser receives it:
    ```bash
    source publish.sh
    ```

## API Endpoints

| Method | Endpoint               | Description                              |
|--------|------------------------|------------------------------------------|
| GET    | /health                | Check the health status of the server    |
| GET    | /                      | Access the home page                     |
| GET    | /vapid-public-key      | Retrieve the VAPID public key            |
| POST   | /publish               | Publish a push notification              |
| POST   | /subscribe             | Subscribe to push notifications          |
| POST   | /unsubscribe           | Unsubscribe from push notifications      |
