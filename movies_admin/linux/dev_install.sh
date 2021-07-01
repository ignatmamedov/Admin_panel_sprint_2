#!/bin/bash
python -m pip install -r /movies_admin/config/settings/requirements.txt
python /movies_admin/manage.py makemigrations movies
python /movies_admin/manage.py migrate movies
python /movies_admin/manage.py migrate
python /movies_admin/manage.py createsuperuser --noinput
python /movies_admin/manage.py shell < /movies_admin/linux/generate_content.py
python /movies_admin/manage.py collectstatic --noinput
python /movies_admin/manage.py runserver 0.0.0.0:8000