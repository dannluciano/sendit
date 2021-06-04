#!/bin/bash

set -e

export DB=senditdb

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -z "$(find -H /var/lib/apt/lists -maxdepth 0 -mtime -7)" ]; then
        echo "==> Install Linux Packages"
        sudo apt-get update
        sudo apt-get upgrade -y
        sudo apt-get install -qq \
            python3 \
            postgresql \
            redis
        sudo apt-get install -qq $(grep -vE "^\s*#" apt-packages | tr "\n" " ")
    fi

    PYTHON_VERSION=$(python3 -c 'import platform; print(platform.python_version())')
    echo "Global Python Version $PYTHON_VERSION"

    if ! [ -x "$(command -v pipenv)" ]; then
        echo "==> Instaling Pipenv"
        pip3 install --user -U pipenv
    fi

    if ! [ -x "$(command -v forego)" ]; then
        echo "==> Instaling Forego"
        wget https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.tgz
        tar xvf forego-stable-linux-amd64.tgz -C /usr/local/bin
        rm -f forego-stable-linux-amd64.tgz
    fi
    
    echo "==> Creating Database if not exists"
    sudo su - postgres -c "psql -U postgres -c 'select 1' -d $DB &>/dev/null || psql -U postgres -tc 'create database $DB'" 

elif [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -x "$(command -v brew)" ]; then
        echo "==> Install MacOS Packages"
        brew list python@3 &>/dev/null || brew install python@3;
        brew list postgresql &>/dev/null || brew install postgresql;
        brew list redis &>/dev/null || brew install redis;
    fi

    echo "==> Creating Database if not exists"
    psql -U postgres -c 'select 1' -d $DB &>/dev/null || psql -U postgres -tc "create database $DB"

else
    echo "==> Operating System not supported!"
fi

pipenv --venv &>/dev/null
if [ $? -eq 1 ]; then
    echo "==> Creating Virtualenv"
    pipenv --python $PYTHON_VERSION
    pipenv install --dev
fi

if [ ! -e "SendIT/settings_local.py" ]; then
    echo "==> Coping Local Settings"
    cp SendIT/settings_local.py.sample SendIT/settings_local.py
fi    

echo "==> Running check, migrate, loaddata and collectstatic"
pipenv run python manage.py check
pipenv run python manage.py migrate --noinput --skip-checks
pipenv run python manage.py loaddata db_core --skip-checks
pipenv run python manage.py collectstatic --noinput


exists_none_users="
from django.contrib.auth.models import User;
if User.objects.count()==0:
    exit(0)
else:
    exit(1);
"
printf "$exists_none_users" | pipenv run python manage.py shell

if [ $? -eq 0 ]; then
    echo "==> Creating Superuser"
    pipenv run python manage.py createsuperuser --skip-checks
fi

mkdir -p temp
echo "==> Finished"
echo "Run 'pipenv run start' to see the magic"
