#!/bin/sh

/app/scripts/setup.sh
if [ \"$${IS_IN_PRODUCTION}\" = '1' ]; then
  gunicorn core.wsgi:application --bind :"${DJANGO_PORT}";
else
  python manage.py runserver 0.0.0.0:"${DJANGO_PORT}";
fi