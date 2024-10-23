#!/bin/bash

set -e

source env_vm/bin/activate

./manage.py download_docker_images

DEBUG=True HIVEMIND_PROCFILE=Procfile.local hivemind --processes worker &
DEBUG=True python manage.py runserver 0.0.0.0:8000
