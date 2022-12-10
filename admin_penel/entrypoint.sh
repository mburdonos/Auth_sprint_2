#!/usr/bin/env bash

if [ "$POSTGRES_DB" = "movies_db" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python sqlite_to_postgres/load_data.py

python manage.py makemigrations
python manage.py migrate --fake movies 0001_initial
python manage.py migrate

python manage.py collectstatic

gunicorn config.wsgi:application --bind 0.0.0.0:7000 --reload -w 4