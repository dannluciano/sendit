#!/bin/bash

set -e

if [ "$(id -u)" -ne 0 ]; then echo "Please run as root." >&2; exit 1; fi

if [ ! -d "/var/www/sendit-worker"  ]; then
    echo "==> Creating Dir /var/www/sendit-worker"
    mkdir -p "/var/www/sendit-worker"
    cd "/var/www/sendit-worker"
    echo "==> Clonning Git"
    git clone --bare /home/dokku/sendittwo
else
    echo "==> Pulling Git"
    cd "/var/www/sendit-worker"
    git pull
fi

if [ ! -d "worker_env"  ]; then
    echo "==> Creating Virtualenv"
    python3 -m venv --prompt "sendit_worker" worker_env
fi

echo "==> Installings Python Deps"
source ./worker_env/bin/activate
python -m pip install -r requirements.txt

python manage.py download_docker_images

echo "==> Installings SystemD Services"
cp ./systemd/rqscheduler.service /etc/systemd/system
cp ./systemd/rqworker@.service   /etc/systemd/system

systemctl daemon-reload
systemctl enable rqscheduler.service
systemctl enable rqworker@1.service
systemctl enable rqworker@2.service
systemctl enable rqworker@3.service
systemctl enable rqworker@4.service

systemctl start rqscheduler.service
systemctl start rqworker@1.service
systemctl start rqworker@2.service
systemctl start rqworker@3.service
systemctl start rqworker@4.service