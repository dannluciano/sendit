#!/bin/sh

if [ "$APP" = "web" ]; then
    echo "==> Migrating Database"
    python3 manage.py migrate --noinput || exit 1

    echo "==> Loading Data do Database"
    python3 manage.py loaddata seeds.json 
fi

if [ "$APP" = "worker" ]; then
    echo "==> Downloading Runtimes"
    python3 manage.py download_docker_images
fi

exec "$@"
