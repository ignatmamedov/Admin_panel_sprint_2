#!/bin/bash
python ./movies_admin/manage.py collectstatic --noinput
docker-compose -f ./src/docker-compose.yml up -d