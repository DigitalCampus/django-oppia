.. _install:

Installation
============

* To install the OppiaMobile server you will first need to have a running Django 
  server installation with both the `South <http://south.aeracode.org/>`_ and 
  `TastyPie <http://tastypieapi.org/>`_ libraries installed. We recommend that 
  you use `virtualenv <https://pypi.python.org/pypi/virtualenv/>`_  to sandbox 
  your python libraries from others on your server.

* Run ``python manage syncdb`` to create the tables for South and TastyPie in 
  your database (if you haven't already done so during their installations)

* Install OppiaMobile, run ``pip install django-oppia``

* Edit your ``settings.py`` file as follows:
	* Add :mod:`oppia`, :mod:`oppia.quiz` and :mod:`oppia.viz` to your 
	  `INSTALLED_APPS` like this::
	
	      INSTALLED_APPS = (
	          ...
	          'oppia',
	          'oppia.quiz',
	          'oppia.viz'
	      )
	* Add the following code::
	
		from oppia import local_settings
		local_settings.modify(globals())
		
	* Ensure you have the following standard Django settings configured:
	
		* `LOGIN_REDIRECT_URL <https://docs.djangoproject.com/en/1.5/ref/settings/#login-redirect-url>`_
		* `SERVER_EMAIL <https://docs.djangoproject.com/en/1.5/ref/settings/#login-url>`_
		* `LOGIN_URL <https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-SERVER_EMAIL>`_
		
	* Add a new setting ``COURSE_UPLOAD_DIR``, this should a read/writable 
	  directory by your webserver user, for example::
	
		COURSE_UPLOAD_DIR = '/home/uploads/'
		
	 This directory will store any uploaded courses, but it should not be web 
	 accessible (the server app will control access to the downloads)

* Include the oppia URLconf in your project ``urls.py`` like this::

      url(r'^', include('oppia.urls')),
      
  It is expected that you would like the app running from the root of your 
  domain name. If this is not the case, then you can alternatively use::
      
      url(r'^oppia/', include('oppia.urls')),
      
  However, you may need to change some of the ``LOGIN_EXEMPT_URLS`` in the 
  ``local_settings.py`` file
      
* Run ``python manage.py migrate oppia``, 
  ``python manage.py migrate oppia.quiz`` and 
  ``python manage.py migrate oppia.viz`` to create the oppia models.

* Run ``python manage.py collectstatic`` this will copy all the required 
  javascript, images, css and other static files are copied to your `STATIC_ROOT`
  
* Run ``python manage.py loaddata default_badges.json`` this will create the 
  default badges in your database.

* Your OppiaMobile server should now be up and running: http://localhost:8000/
  (or at http://localhost:8000/oppia depending on how you configured your 
  ``urls.py`` file)

.. _installcron:

* Finally you should set up a `cron <https://en.wikipedia.org/wiki/Cron>`_ 
  task to run the ``oppia/cron.py`` script regularly. 
  This script tidies up the course download directory of temporary download 
  files and also checks which course badges should be awarded.

	* Exactly how you call ``cron.py`` will depend on your environment, but as 
	  an example on my development server (and using virtualenv) I use a 
	  wrapper shell script with the following content::
	
		#!/bin/bash

		cd /home/alex/data/development/home_alexlittle_net/venv/ # <- path to my virtualenv
		source bin/activate # <- activate the virtualenv
		
		PYTHONPATH="${PYTHONPATH}:/home/alex/data/development/" # <- path to my Django project root

		export PYTHONPATH
		export DJANGO_SETTINGS_MODULE=home_alexlittle_net.settings # <- my main Django settings (relative to the Django project path)

		python /home/alex/data/development/django-oppia/oppia/cron.py # <- full path to the cron.py file 
		
	* This script handles activating the virtualenv correctly and ensuring all 
	  the Django modules/apps can be accessed. I then have my cron call this 
	  wrapper script every 2 hours.
