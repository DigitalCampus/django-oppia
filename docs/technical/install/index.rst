.. _install:

Installation
============

To install and run the OppiaMobile server, you will need to be familiar with how
to set up, install and maintain Django applications. To learn how to get started 
with Django, visit http://www.gettingstartedwithdjango.com/.


* Create a virtual environment for python. We recommend that 
  you use `virtualenv <https://pypi.python.org/pypi/virtualenv/>`_  to sandbox 
  your python libraries from others on your server.
  
* Create a fork of the `django-oppia <https://github.com/DigitalCampus/django-oppia>`_ 
  repository on Github and check this out to your server. For more information 
  on how to fork a repository in GitHub, see: https://help.github.com/articles/fork-a-repo/

* Run ``python setup.py develop`` to install the dependencies

* Add `oppia` to your installed `INSTALLED_APPS` like this::

          INSTALLED_APPS = (
              ...
              'oppia',
          )

* Edit your Django ``settings.py`` file as follows:
    * Add::
    
    	import os,sys
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	PROJECT_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'django-oppia'))
	if PROJECT_PATH not in sys.path:
		sys.path.insert(0, PROJECT_PATH)
    
      replacing `django-oppia` with the name of your fork in github and 
      referencing the location on your server where you have cloned the repository
    
    * Add the following code::
	
		from oppia import local_settings_live
		local_settings_live.modify(globals())
		
    * Ensure you have the following standard Django settings configured:
	
		* `LOGIN_REDIRECT_URL <https://docs.djangoproject.com/en/1.11/ref/settings/#login-redirect-url>`_
		* `SERVER_EMAIL <https://docs.djangoproject.com/en/1.11/ref/settings/#server-email>`_
		* `LOGIN_URL <https://docs.djangoproject.com/en/1.11/ref/settings/#login-url>`_
		
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
      
* Run ``python manage.py migrate`` to create the oppia models.

* Run ``python manage.py collectstatic`` this will copy all the required 
  javascript, images, css and other static files are copied to your `STATIC_ROOT`
  
* Run ``python manage.py createsuperuser`` to create the admin user for your site

* Run ``python manage.py loaddata default_badges.json`` this will create the 
  default badges in your database.

* Your OppiaMobile server should now be up and running: http://localhost:8000/
  (or at http://localhost:8000/oppia depending on how you configured your 
  ``urls.py`` file)

* Finally, contribute! If you find issues and have fixed them, then please send 
  us a pull request to integrate into the core server code so everyone can 
  benefit. If you find an issue, but aren't sure how to fix it, then please 
  `file an issue on Github <https://github.com/DigitalCampus/django-oppia/issues>`_

.. _installcron:  

Cron
---------


You should set up a `cron <https://en.wikipedia.org/wiki/Cron>`_ task to run the
``oppia/cron.py`` script regularly. This script tidies up the course download 
directory of temporary download files and also checks which course badges 
should be awarded.

* Exactly how you call ``cron.py`` will depend on your environment, but as 
  an example on our development server (and using virtualenv) we use a 
  wrapper shell script with the following content::

	#!/bin/bash

	cd /home/alex/data/development/oppia_core/env/ # <- path to virtualenv
	source bin/activate # <- activate the virtualenv
	
	PYTHONPATH="${PYTHONPATH}:/home/alex/data/development/" # <- path to Django project root

	export PYTHONPATH
	export DJANGO_SETTINGS_MODULE=oppia_core.settings # <- main Django settings (relative to the Django project path)

	python /home/alex/data/development/django-oppia/oppia/cron.py # <- full path to the cron.py file 
	
* This script handles activating the virtualenv correctly and ensuring all 
  the Django modules/apps can be accessed. We then have my cron call this 
  wrapper script every 2 hours.
