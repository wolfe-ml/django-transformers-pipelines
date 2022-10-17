#!/bin/sh

set -e

python example_project/manage.py makemigrations
python example_project/manage.py migrate
python example_project/manage.py runserver
