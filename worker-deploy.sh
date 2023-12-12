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

cp ./systemd/sendit-rqscheduler.service /etc/systemd/system
cp ./systemd/sendit-mem-db.service      /etc/systemd/system
cp ./systemd/sendit-per-db.service      /etc/systemd/system
cp ./systemd/sendit-rqworker@.service   /etc/systemd/system

echo "==> Reload SystemD Daemons"
systemctl daemon-reload

echo "==> Enabling Services"
systemctl enable sendit-mem-db.service
systemctl enable sendit-per-db.service

systemctl enable sendit-rqscheduler.service
systemctl enable sendit-rqworker@1.service
systemctl enable sendit-rqworker@2.service
systemctl enable sendit-rqworker@3.service
systemctl enable sendit-rqworker@4.service

echo "==> Starting Services"

systemctl start sendit-mem-db.service
systemctl start sendit-per-db.service

systemctl start sendit-rqscheduler.service

systemctl start sendit-rqworker@1.service
systemctl start sendit-rqworker@2.service
systemctl start sendit-rqworker@3.service
systemctl start sendit-rqworker@4.service

echo "==> Done"