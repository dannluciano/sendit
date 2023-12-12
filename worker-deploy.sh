#!/bin/bash

set -e

git pull

if [ ! -d "worker_env"  ]; then
    echo "==> Creating Virtualenv"
    python3 -m venv --prompt "sendit_worker" worker_env
fi

source ./worker_env/bin/activate
python -m pip install -r requirements.txt

python manage.py download_docker_images

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