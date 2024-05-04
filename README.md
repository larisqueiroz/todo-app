# todo-app
A To do list API in Python using Django.

## Description
This is a todo application API and it's possible to search, create, edit and delete users (if superuser), tasks, cards and tags.

## ER Diagram
![ER.png](screenshots%2FER.png)

## Built with
* Python
* Django
* SQLite DB
* Postman

## Features
* Authentication using Django's TokenAuthentication 
* CRUD Tasks
* CRUD Users
* CRUD Tags
* CRUD Cards

## Getting Started
1. Clone this repository.
2. Install requirements:
```
pip freeze > requirements.txt
```
3. On project root, run:
```
python manage.py runserver
```
4. Use postman to send requisitions from http://localhost:8000

## URLs
* http://localhost:8000/tags
* http://localhost:8000/tags/{id}
* http://localhost:8000/tasks
* http://localhost:8000/tasks/{id}
* http://localhost:8000/cards
* http://localhost:8000/cards/{id}
* http://localhost:8000/cards/{id}/tasks
* http://localhost:8000/users
* http://localhost:8000/users/{id}
* http://localhost:8000/users/{id}/cards
* http://localhost:8000/users/{id}/tags
* http://localhost:8000/login
* http://localhost:8000/logout

## User admin for protected requests
username: admin \
password: admin

PS: Database is already populed with some data.