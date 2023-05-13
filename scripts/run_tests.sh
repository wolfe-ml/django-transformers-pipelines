#!/bin/sh

set -e


coverage run boot_django.py test
coverage report
