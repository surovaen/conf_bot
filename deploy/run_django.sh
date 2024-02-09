#!/bin/sh

python "manage.py" collectstatic --noinput

python "manage.py" migrate --noinput

python "manage.py" setuptasks

gunicorn -c "$PROJECT_ROOT/gunicorn.conf.py" server.wsgi:application
