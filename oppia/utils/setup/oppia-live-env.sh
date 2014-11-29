#!/bin/bash

cd /home

sudo django-admin startproject nurhi

sudo chown -R ubuntu:ubuntu nurhi/

cd nurhi/

mkdir static
mkdir uploads
mkdir media

change ownership of uploads & media to be ubuntu:www-data

virtualenv env
source env/bin/activate

pip install django==1.6.6 south django-tastypie django-tablib django-crispy-forms mysql-python


git clone https://github.com/DigitalCampus/django-nurhi-oppia.git

Fix up :

urls.py
wsgi.py
settings.py


python manage.py collectstatic

python manage.py syncdb

python manage.py migrate


create apache site(s)






