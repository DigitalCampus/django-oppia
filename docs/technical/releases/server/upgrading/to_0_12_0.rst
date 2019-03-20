Migrating to Python 3 and Django 2
=====================================

To migrate to using OppiaMobile v0.12.0, you will need to update the versions
or Python and Django that you are using. The migration steps are described 
below, running the commands from the root of your OppiaMobile server 
installation (eg ``/home/oppia/``).

Update virtualenv
---------------------

#. Remove the existing virtualenv: ``$ sudo rm -R env``
#. Create a new virtualenv: ``$ virtualenv -p /usr/bin/python3 env``
#. Activate the new virtualenv: ``$ source env/bin/activate``

Update MySQL connectors
------------------------

The MySQL connector libraries in Python 3 have been changed:

#. Run: ``$ sudo apt-get install python3-mysqldb python3-dev libpython3-dev``
#. Run: ``(env)$ pip install mysqlclient``

Update Pillow dependencies
---------------------------

The new version of Oppia uses an updated version of Pillow, so you may need to 
update the Pillow dependencies to ensure the new version installs correctly:

#. Run: ``$ sudo apt-get install libjpeg-dev zlib1g-dev``


Add required Oppia packages
----------------------------

Since we have removed the old virtualenv, we need to re-install, and at the 
same time, update the required packages:

#. Run: ``(env)$ pip install -r ../django-oppia/requirements.txt``


For live servers using mod_wsgi on Apache webserver
----------------------------------------------------

If you are running

sudo apt-get install libapache2-mod-wsgi-py3

Also update the path in the apache config file to the python site packages







