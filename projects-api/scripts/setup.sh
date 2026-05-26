#! /bin/bash

set -e

if [ "$(uname)" == "Darwin" ]; then
    echo "==> OSX"
    brew install --cask docker
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "==> Linux"
    SUDO=''
    if (( $EUID != 0 )); then
        SUDO='sudo'
    fi
    $SUDO 'apt install docker'
else
    echo "==> Plataform not Supported"
fi

echo "==> Start Service"
docker-compose up