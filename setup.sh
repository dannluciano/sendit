#!/bin/bash

set -e

export DB=senditdb

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export ARCH=$(uname -m)
    if [ -z "$(find -H /var/lib/apt/lists -maxdepth 0 -mtime -7)" ]; then
        echo "==> Install Linux Packages"
        sudo apt-get update
        sudo apt-get upgrade -y
        sudo apt-get install -qq \
            python3 \
            postgresql \
            libpq-dev \
            redis \
            wget \
            git \
            python3-dev \
            python3-venv
        sudo apt-get install -qq $(grep -vE "^\s*#" apt-packages | tr "\n" " ")
    fi

    PYTHON_VERSION=$(python3 -c 'import platform; print(platform.python_version())')
    echo "Global Python Version $PYTHON_VERSION"

    if ! [ -x "$(command -v hivemind)" ]; then
        echo "==> Instaling Forego"
        wget "https://github.com/DarthSim/hivemind/releases/download/v1.1.0/hivemind-v1.1.0-linux-arm64.gz"
        gunzip hivemind-v1.1.0-linux-arm64.gz
        rm -f hivemind-v1.1.0-linux-arm64.gz
        sudo mv hivemind-v1.1.0-linux-arm64 /usr/local/bin/hivemind
        sudo chmod +x /usr/local/bin/hivemind
    fi
    
    echo "==> Creating Database if not exists"
    sudo su - postgres -c "psql -U postgres -c 'select 1' -d $DB &>/dev/null || psql -U postgres -tc 'create database $DB'" 

elif [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -x "$(command -v brew)" ]; then
        echo "==> Install MacOS Packages"
        brew list python@3 &>/dev/null || brew install python@3;
        brew list postgresql &>/dev/null || brew install postgresql;
        brew list redis &>/dev/null || brew install redis;
        brew list forego &>/dev/null || brew install forego;
        brew services
        brew services start postgresql
        brew services start redis
    fi

    echo "==> Creating Database if not exists"
    psql -U postgres -c 'select 1' -d $DB &>/dev/null || psql -U postgres -tc "create database $DB"

else
    echo "==> Operating System not supported!"
fi

if [ ! -d "env_vm"  ]; then
    echo "==> Creating Virtualenv"
    python3 -m venv --prompt "sendit" env_vm
    source env_vm/bin/activate
    python3 -m pip install -r requirements.dev.txt
    python3 -m pip install -r requirements.txt
else
    source env_vm/bin/activate
fi

if [ ! -e "SendIT/settings_local.py" ]; then
    echo "==> Coping Local Settings"
    cp SendIT/settings_local.py.sample SendIT/settings_local.py
fi    

echo "==> Running check, migrate, loaddata and collectstatic"
python manage.py check
python manage.py migrate --noinput --skip-checks
python manage.py loaddata db_core --skip-checks
python manage.py collectstatic --noinput


exists_none_users="
from django.contrib.auth.models import User;
if User.objects.count()==0:
    exit(0)
else:
    exit(1);
"
printf "$exists_none_users" | python manage.py shell

if [ $? -eq 0 ]; then
    echo "==> Creating Superuser"
    python manage.py createsuperuser --skip-checks
fi

mkdir -p temp
echo "==> Finished"
echo "Run './run.sh' to see the magic"
