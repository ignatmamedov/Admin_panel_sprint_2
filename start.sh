#!/bin/bash
sed -i -e 's/\r$//' ./movies_admin/linux/dev_install.sh
python ./movies_admin/manage.py collectstatic --noinput
docker-compose -f ./src/docker-compose.yml up -d
