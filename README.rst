===========
OppiaMobile
===========

OppiaMobile is the server side component for the OppiaMobile learning application

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "oppia" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'oppia',
      )

2. Include the oppia URLconf in your project urls.py like this::

      url(r'^oppia/', include('oppia.urls')),

3. Run `python manage.py syncdb` to create the oppia models.

4. Start the development server and visit http://127.0.0.1:8000/admin/ 
   (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/oppia/ 
