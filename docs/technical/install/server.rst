Server - Manual Installation
==============================

To manual install and run an OppiaMobile server, e.g. as a local development
server or as live server running on a locally hosted server. Please follow the
instructions below.

Prerequisites
-----------------

It would be helpful if you had some system admin/set up experience before, and 
please note that these instructions are based on using Ubuntu as the 
operating system, with MySQL for the database server and Apache2 as the 
webserver. If you are using a different operating system, database or 
webserver, then some of the exact commands may differ a little.

You should have some familiarity with `Git <https://git-scm.com/>`_ and have 
this installed on your machine.

1. Set up empty database
------------------------

We generally use MySQL for the database, but Oppia will support any database
platform that Django supports (see: 
https://docs.djangoproject.com/en/2.1/ref/databases/ for more detailed notes)

In the MySQL command line, run::

	> create database oppia default character set utf8mb4;
	> grant all privileges on oppia.* to 'oppiauser'@'localhost' identified by 
		'yourpassword';
	> flush privileges;
	> quit

The database name, username and password can be whatever you like.

2. Clone the code and add custom settings
------------------------------------------

Select or create a suitable directory on your file system, for the rest of this 
setup. We use ``/home/oppia/``, but you may prefer something like 
``/var/html/oppia/``. The rest of these instructions will assume you are using 
``/home/oppia/``, so edit any of the following commands/settings as necessary
if you're using something different.

#. Navigate to your selected directory
#. Run::
	
    $ git clone https://github.com/DigitalCampus/django-oppia.git
	
   If you have your own fork of the Oppia code, then replace the location with 
   your own fork's url.
   
#. This will create a directory ``/home/oppia/django-oppia/`` with the latest
   stable release version of the Oppia server code.   
#. Navigate to the ``/home/oppia/django-oppia/oppiamobile/`` directory
#. Copy the ``settings_secret.py.template`` to ``settings_secret.py``, eg:
   by using::
   
   	$ cp settings_secret.py.template settings_secret.py

#. Open the ``settings_secret.py`` file in your favourite text editor and
   update at least the following settings:
   
   #. Database name, user, password (that you created in step 1 above)
   #. SECRET_KEY. This can be anything you like, generally a long list of 
      random characters.
   #. ADMINS and SERVER_EMAIL - update these to your system admin details
   
   In this file you can override any of the settings in 
   ``/home/oppia/django-oppia/oppiamobile/settings.py``
   
#. Save your ``settings_secret.py`` file
    
   
3. Set up virtualenv and packages
-----------------------------------

`VirtualEnv <https://pypi.python.org/pypi/virtualenv/>`_  is a way to sandbox
your python libraries so they are not affected by other updates or versions
that you may be using for other services and applications on your machine. You
don't have to use this, but it is very strongly recommended that you download
and install this to use.

#. Navigate to ``/home/oppia/`` and run::
	
	$ virtualenv env
	
#. Run::

	$ source env/bin/activate
	
   Your command line should now look something like::
  
    (env)$

#. Install the required packages for the Oppia server by running::

    (env)$ pip install -r django-oppia/requirements.txt
    
   This may take some time as it downloads and sets up all the necessary
   python libraries that are required by the Oppia server
   
#. Install a database connector, since we use MySQL, the command below is 
   specifically for that database server. If you are using a different database 
   server, then use the appropriate one for your database server::
   
    (env)$ pip install mysql-python
    
#. You should now have all the required libraries set up and installed. 


4. Set up other directories and permissions
---------------------------------------------

Create directories for media, static and uploads by running (from 
``/home/oppia/``)::
	
	$ mkdir media
	$ mkdir static
	$ mkdir upload

If you are going to run this Oppia server as a live server, you should make 
sure that your webserver user (eg www-data) had read and write access to all
these directories.

5. Initialise the database and add admin user
-----------------------------------------------

Now to create the database structure and an initial admin user.

#. Navigate the ``/home/oppia/django-oppia/`` directory
#. Create the database by running::

	(env)$ python manage.py migrate
	
#. Copy the static files with::

	(env)$ python manage.py collectstatic

#. Create a first admin user with::

	(env)$ python manage.py createsuperuser

   and follow the instructions.

6. Run the tests (optional but recommended)
---------------------------------------------

To check that everything has been set up and installed correctly, you can run 
the automated tests using::

	(env)$ python manage.py test

7. Test running the server locally
-------------------------------------

Check that the server will run properly on the local machine, by running::

	(env)$ python manage.py runserver

Then, in the web browser on the same machine, open::

	http://localhost:8000 


8. Configure web server (for live servers)
--------------------------------------------

If the Oppia server you are setting up is to run as a live server, then you 
will need to configure your web server.

As mentioned above, these instructions assume that you are using Apache 
webserver, and we use the 
`mod_wsgi <https://modwsgi.readthedocs.io/en/latest/>`_ 
package for serving python applications via Apache, so before proceeding, 
ensure that you have mod_wsgi installed and enabled for your Apache server.

Here is an example Apache config file that you can use and adapt::

	<VirtualHost *:80>
	
		ServerName localhost.oppia
		WSGIDaemonProcess localhost.oppia python-path=/home/oppia/django-oppia:/home/oppia/env/lib/python2.7/site-packages
		WSGIProcessGroup localhost.oppia
		WSGIScriptAlias / /home/oppia/django-oppia/oppiamobile/wsgi.py
		WSGIPassAuthorization On
	
		<Directory /home/oppia/django-oppia/oppiamobile/>
			<Files wsgi.py>
				Require all granted
			</Files>
		</Directory>
	
		Alias /media /home/oppia/media/
	    	<Directory "/home/oppia/media/">
			Options MultiViews FollowSymLinks
			AllowOverride None
			Require all granted
	    	</Directory>
	
		Alias /static /home/oppia/static/
	    	<Directory "/home/oppia/static/">
			Options MultiViews FollowSymLinks
			AllowOverride None
			Require all granted
	    	</Directory>
	
		
	
		LogLevel warn
		ErrorLog /var/log/apache2/oppia-core-error.log
		CustomLog /var/log/apache2/oppia-core-access.log combined
	
	</VirtualHost>

Replace the ``ServerName`` ``localhost.oppia`` with your site's domain name and
adjust any instances of ``/home/oppia/`` with the directory you used for 
installing.

.. _installcron:

9. Set up cron tasks
---------------------

There are 2 cron tasks, one does the processing for awarding badges and general 
maintenance (eg clearing old user sessions and temporary files), and the other 
to generate the cached data for displaying the dashboard data.

Here are 2 example files that you can use, for each of these cron tasks. We 
recommend putting these files in your ``/home/oppia/`` directory.

``cron.sh``::
 
	#!/bin/bash

	cd /home/oppia/
	source env/bin/activate
	
	python django-oppia/manage.py oppiacron --hours=48
	
``cron-summary.sh``::
 
	#!/bin/bash

	cd /home/oppia/
	source env/bin/activate
	
	python django-oppia/manage.py update_summaries

10. Contribute!
----------------

If you find issues and have fixed them or have added extra features/
functionality, then please send us a pull request to integrate into the core 
server code so everyone can benefit. If you find an issue, but aren't sure how 
to fix it, then please 
`file an issue on Github <https://github.com/DigitalCampus/django-oppia/issues>`_

If you need any help, then please post a message on the 
`OppiaMobile Google Group <https://groups.google.com/forum/#!forum/oppiamobile>`_ 

