Migrating to Python 3 and Django 2
=====================================

These are basic notes/reference as I test and update the Oppia code

Update virtual env
---------------------

virtualenv -p /usr/bin/python3 env
source env/bin/activate

Add Mysql connectors...
------------------------

sudo apt-get install python3-mysqldb
sudo apt-get install python3-dev libpython3-dev
pip install mysqlclient

Fix Pillow dependencies
------------------------

sudo apt-get install libjpeg-dev
sudo apt-get install zlib1g-dev


Add required packages
----------------------

pip install -r ../django-oppia/requirements.txt


on live server might need new version of mod_wsgi:

sudo apt-get install libapache2-mod-wsgi-py3







