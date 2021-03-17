REDIS_HOST=localhost
REDIS_PORT=6379
gunicorn -b 0.0.0.0:8080 -k flask_sockets.worker main:app
