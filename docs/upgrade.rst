Upgrading
=========

Before you upgrade, if you have made any changes to your ``local_settings.py`` 
file (for example to add your Google Analytics tracking code or turning off self
registration) then you should backup your local settings as these may get 
overwritten during the upgrade process.

To upgrade django-oppia, we recommend that you first uninstall the old version 
(``pip uninstall django-oppia``) and then install the new version (``pip install django-oppia``).

If you try to upgrade (``pip install --upgrade django-oppia``), it may also 
reinstall some of the dependency packages (TastyPie etc).

Once you have reinstalled OppiaMobile, run ``python manage.py migrate oppia``, 
``python manage.py migrate oppia.quiz`` and  ``python manage.py migrate oppia.viz`` 
to apply any database updates.

You should also then put back any changes to your ``local_settings.py`` file.

Run ``python manage.py collectstatic`` this will copy all the required 
javascript, images, css and other static files are copied to your `STATIC_ROOT`.