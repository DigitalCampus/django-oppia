Testing Process for OppiaMobile Server
=======================================

The Oppia server uses `Django's inbuilt unit testing framework <https://docs.djangoproject.com/en/1.11/topics/testing/overview/>`_ .

All the unit tests can be found under: https://github.com/DigitalCampus/django-oppia/tree/master/oppia/tests

Run the tests on your Oppia server
-----------------------------------

#. Activate the virtual environment (eg: ``/home/www/oppia/$ source env/bin/activate``)
#. Run all the tests with ``python manage.py test oppia.tests`` 


Adding more tests
-------------------

If you are adding additional functionality to the Oppia server, you can add tests for this functionality using the 
standard Django unit testing framework.
