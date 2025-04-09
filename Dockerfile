FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y build-essential curl && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get remove -y build-essential && apt-get autoremove -y && apt-get clean

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "/app/web-entrypoint.sh"]
