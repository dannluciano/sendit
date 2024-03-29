#!/bin/bash

set -e

source env_vm/bin/activate

DEBUG=True python manage.py runserver
