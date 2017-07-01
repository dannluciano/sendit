# sendit

1. Se não estiver o pip instalado execute: ```python get-pip.py install```
2. Após isto, instale o virtualenv: ```pip install virtualenv```
3. Crie um virtualenv com o comando ```python3.6 -m venv env```
4. Instale as dependencias do projeto ```pip install -r requeriments.txt```
5. Depois entre na pasta SendIT ```cd SendIT```
6. Crie a Base de Dados ```python manage.py migrate````
7. Inicialize a Base de Dados ```python manage.py loaddata see```
8. Crie o super Usuario do Admin ```python manage.py createsuperuse```
9. Rode o servidor ```python manage.py runserve```
10. Abra o navegador na url ```localhost:8000/```
