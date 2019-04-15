# sendit

1. Se não estiver o pip instalado execute: 
```python get-pip.py install```
2. Após isto, instale o pipenv: 
```pip install pipenv```
3. Crie um virtualenv e as instale as dependencias do projetocom o comando 
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
9. Rode o servidor 
```python manage.py runserver```
11. Abra o navegador na url 
```localhost:8000/```
