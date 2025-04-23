#!/bin/sh

# Start Django
python manage.py migrate
uvicorn nlpgrad.asgi:application --host 0.0.0.0 --port 8000