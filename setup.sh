#!/bin/bash

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

if ! [ -x "$(command -v pipenv)" ]; then
    echo "==> Instaling Pipenv"
    pip install --user -U pipenv
fi

if ! [ -x "$(command -v forego)" ]; then
    echo "==> Instaling Forego"
    wget https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.tgz
    tar xvf forego-stable-linux-amd64.tgz -C /usr/local/bin
    rm -f forego-stable-linux-amd64.tgz
fi

pipenv --venv &>/dev/null
if [ $? -eq 1 ]; then
    echo "==> Creating Virtualenv"
    pipenv --python 3
    pipenv install --dev
fi

if [ ! -e "SendIT/settings_local.py" ]; then
    echo "==> Coping Local Settings"
    cp SendIT/settings_local.py.sample SendIT/settings_local.py
fi    

echo "==> Creating Database if not exists"
DB=senditdb
sudo su - postgres -c "psql -U postgres -c 'select 1' -d $DB &>/dev/null || psql -U postgres -tc 'create database $DB'" 

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
