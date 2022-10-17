#!/bin/sh

set -e


python django_ml_project/manage.py test django_inference
