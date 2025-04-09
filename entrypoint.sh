#!/bin/bash
set -e

python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn app.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60
