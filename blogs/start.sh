#!/bin/sh

python manage.py makemigrations
python manage.py migrate  --noinput

if [ $# -gt 0 ]; then
    exec "$@"
else
    python manage.py runserver 0.0.0.0:8080 
    tail -f /dev/null
fi