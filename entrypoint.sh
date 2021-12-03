#!/bin/sh

python massassi-django/manage.py collectstatic --noinput

# run the CMD (gunicorn in this case)
exec "$@"

