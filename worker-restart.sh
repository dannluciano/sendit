#!/bin/bash

set -e

if [ "$(id -u)" -ne 0 ]; then echo "Please run as root." >&2; exit 1; fi

echo "==> Restarting Services"

systemctl restart sendit-mem-db.service
systemctl restart sendit-per-db.service

systemctl restart sendit-rqscheduler.service

systemctl restart sendit-rqworker@1.service
systemctl restart sendit-rqworker@2.service
systemctl restart sendit-rqworker@3.service
systemctl restart sendit-rqworker@4.service

echo "==> Done"
