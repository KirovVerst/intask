# intask
[![Build Status](https://travis-ci.org/KirovVerst/intask.svg?branch=master)](https://travis-ci.org/KirovVerst/intask)
[![Coverage Status](https://coveralls.io/repos/github/KirovVerst/intask/badge.svg?branch=master)](https://coveralls.io/github/KirovVerst/intask?branch=master)

My TaskManager

## Backend
### Requirements
1. Python 3.5

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
Loading test data
```bash
$ python manage.py loaddata fixtures/*
```
### Development 
#### Server
```bash
$ python manage.py runserver
```
### API documentation
Link: `/api/v1/docs/`
