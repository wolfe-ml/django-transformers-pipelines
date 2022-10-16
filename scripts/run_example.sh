#!/bin/sh

set -e


python django_ml_project/manage.py makemigrations
python django_ml_project/manage.py migrate
python django_ml_project/manage.py runserver
