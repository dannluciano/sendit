#!/bin/bash

set -e

source env_vm/bin/activate

./manage.py download_docker_images

PORT=8000 DEBUG=False HIVEMIND_PROCFILE=Procfile.local hivemind