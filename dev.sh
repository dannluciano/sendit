#!/bin/bash

set -e

source env_vm/bin/activate

PORT=8002 DEBUG=True python manage.py runserver 0.0.0.0:8002
