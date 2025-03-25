#!/bin/sh
echo "Django setup running"
python /app/manage.py makemigrations
python /app/manage.py migrate
python /app/manage.py makemigrations core
python /app/manage.py migrate core