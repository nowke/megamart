# Mega-mart #

A Retail store management system

## Installation steps ##

### Clone the repo ###

```sh
$ git clone https://bitbucket.org/nowke/mega-mart
$ cd mega-mart
```
### Setup virtual environment
```sh
$ mkvirtualenv megamart
$ workon megamart
```

### Install requirements
```sh
$ pip install -r requirements.txt
```

### Run django-specific commands
```sh
$ ./manage.py collectstatic
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver
```
