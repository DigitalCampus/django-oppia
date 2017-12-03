.. _upgrade_server:

Upgrading OppiaMobile Server
=============================

To ensure you get all the latest features, bug fixes and patches, it's important to keep your OppiaMobile server up to 
date.

The upgrade process is described below, with the paths/directories described as OppiaMobile server is set up on both the 
AWS and VirtualBox machine images. If you have installed OppiaMobile server to different location, then amend the 
paths/directories as required. Or, if you have your own clone of the OppiaMobile server code, you will need to merge the 
core version into your clone and resolve any conflicts, before updating your server.

Your server must be connected to the internet for the upgrade process.

Backup
-------

Ensure you have a backup of your OppiaMobile database, code and any uploaded files/courses

Pull the latest updates from the core version
----------------------------------------------

#. Move to the django-oppia directory: ``$ cd /home/oppiamobile/django-oppia/``
#. Pull the latest updates: ``$ sudo git pull``

Activate the VirtualEnv
--------------------------

#. Move to Oppia directory: ``$ cd /home/oppiamobile``
#. Activate virtual environment: ``$ source env/bin/activate``

You will see the prefix ``(env)`` at the beginning of your command line. Once the upgrade is complete you can 
de-activate the virtual environment using ``(env)$ deactivate``.

Check for any updated/new required packages
---------------------------------------------

#. Check and install: ``(env)$ pip install -r django-oppia/requirements.txt``

Any updated or new packages will now be installed

Migrate the database
-----------------------

#. Move to oppia_web directory: ``(env)$ cd /home/oppiamobile/oppia_web``
#. Migrate database with: ``(env)$ python manage.py migrate``

Copy static files
------------------

#. Copy static files with: ``(env)$ python manage.py collectstatic``

Restart Apache
------------------

#. Restart Apache server: ``$ sudo service apache2 restart``
