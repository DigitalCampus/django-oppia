#!/bin/sh

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Starting Django Server...'
exec "$@"