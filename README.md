# intask
My TaskManager

##Backend
### Requirements
1. Python 3.*
2. MySQL

###Installation
Python dependencies
```bash
$ pip install -r requirements.txt
```
Database configuration
```bash
$ cd db && mv my.example.cnf my.cnf
```
Migrations
```bash
$ python manage.py migrate
```
###Development server
```bash
$ python manage.py runserver
```

