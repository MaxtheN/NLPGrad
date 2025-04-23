Add ``.env`` file to the root directory. Contents:
```
SECRET_KEY=super_secret_key
DEBUG=True
REDIS_HOST=redis
REDIS_PORT=6379
LLM_API_KEY=abcd1234

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
run ``chmod +x web-entrypoint.sh`` if you are on linux
Just run ``docker compose up``
wait a bit and run ``test.html`` after everything is done
