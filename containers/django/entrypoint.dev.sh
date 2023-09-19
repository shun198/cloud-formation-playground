#!/bin/sh
set -eu

poetry run python manage.py makemigrations
poetry run python manage.py migrate

poetry run gunicorn project.wsgi:application --bind 0.0.0.0:8000