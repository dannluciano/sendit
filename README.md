# sendit

1. Instale Python >= 3.6 e PostgreSQL 11:
    no Linux ou no Windows SubfileSystem Linux (WSL):
```apt install python3 postgresql```
    no Mac OS:
```brew install python3 postgresql```
2. Após isto, instale o pipenv: 
```pip install pipenv```
3. Crie um virtualenv e as instale as dependencias do projeto
```pipenv --python 3.6```
```pipenv install```
4. Depois entre na pasta SendIT 
```cd SendIT```
5. Crie a Base de Dados 
```python manage.py migrate```
6. Inicialize a Base de Dados 
```python manage.py loaddata seed```
7. Crie o super Usuario do Admin 
```python manage.py createsuperuser```
8. Colete os Arquivos Estaticos 
```python manage.py collectstatic```
9. Criar pasta temporaria
```mkdir temp```
10. Rode o servidor web
    em modo de desenvolvimento:
```python manage.py runserver```
    em modo de produção:
```gunicorn -b 0.0.0.0:8000 -w 16 -t 30 --preload --capture-output --access-logfile - --log-file - SendIT.wsgi```
11. Abra o navegador na url 
```localhost:8000/```
