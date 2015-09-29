# Mega-mart #

A Retail store management system

## Installation steps ##

### Clone the repo ###

```
#!bash

$ git clone https://bitbucket.org/nowke/mega-mart
$ cd mega-mart
```
### Setup virtual environment
```
#!bash
$ mkvirtualenv megamart
$ workon megamart
```

### Install requirements
```
#!bash
$ pip install -r requirements.txt
```

### Run django-specific commands
```
#!bash
$ python manage.py collectstatic
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```