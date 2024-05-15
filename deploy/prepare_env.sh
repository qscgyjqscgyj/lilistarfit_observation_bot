#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py createsuperuser_seed
