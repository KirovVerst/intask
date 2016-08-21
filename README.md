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
Database config
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
###API documentation
Link: `/api/v1/docs/`
