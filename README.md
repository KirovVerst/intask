# intask
My TaskManager

##Backend
### Requirements
1. Python 3
2. MySQL

###Installation
Python dependencies
```bash
$ pip install -r requirements.txt
```
Application configuration
```bash
$ cp intask/conf_demo.py intask/conf.py
```
Database configuration
```bash
$ cp db/my.example.cnf db/my.cnf
```
Migrations
```bash
$ python manage.py migrate
```
###Development 
#### Server
```bash
$ python manage.py runserver
```
#### Celery
```
$ celery -A intask worker -l info
```
###API documentation
Link: `/api/v1/docs/`
