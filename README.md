# intask
[![Build Status](https://travis-ci.org/KirovVerst/intask.svg?branch=master)](https://travis-ci.org/KirovVerst/intask)
[![Coverage Status](https://coveralls.io/repos/github/KirovVerst/intask/badge.svg?branch=master)](https://coveralls.io/github/KirovVerst/intask?branch=master)

My TaskManager

## Backend
### Requirements
1. Python 3.5
2. Redis
3. RabbitMQ

### Installation
Python dependencies
```bash
$ pip install -r requirements.txt
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
$ celery multi start w1 -A intask 
$ python manage.py runserver
```
### API documentation
Link: `/api/v1/docs/`

## Frontend
### Installation
```
$ npm install
```
### Build
```
$ npm run build-prod
```
### Tests
```
$ ng test
```
## Licensing
The code in this project is licensed under MIT license.
