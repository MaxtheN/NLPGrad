#!/bin/sh

# Wait for Ollama to be up
echo "Waiting for Ollama to be ready..."
until curl -s http://ollama:11434/api/generate > /dev/null; do
    sleep 2
done

echo "🧠 Pulling orca-mini from web container..."
curl -X POST http://ollama:11434/api/pull -H "Content-Type: application/json" -d '{"name": "orca-mini"}'

# Start Django
python manage.py migrate
uvicorn nlpgrad.asgi:application --host 0.0.0.0 --port 8000