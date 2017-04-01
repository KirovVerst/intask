# intask
[![Build Status](https://travis-ci.org/KirovVerst/intask.svg?branch=master)](https://travis-ci.org/KirovVerst/intask)

My TaskManager

## Backend
### Requirements
1. Python 3.6

### Installation
Python dependencies
```bash
$ pip install -r requirements.txt
```
Application configuration
```bash
$ cp intask/conf_demo.py intask/conf.py
```
Migrations
```bash
$ python manage.py migrate
```
### Development 
#### Server
```bash
$ python manage.py runserver
```
### API documentation
Link: `/api/v1/docs/`
