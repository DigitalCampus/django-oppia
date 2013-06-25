Upgrading
=========

To upgrade django-oppia, we recommend that you first uninstall the old version (``pip uninstall django-oppia``) and then 
install the new version (``pip install django-oppia``).

If you try to upgrade (``pip install --upgrade django-oppia``) , it may also reinstall TastyPie and you'll need to reapply the timezone fix.

Once you have reinstalled OppiaMobile, run ``python manage.py migrate oppia`` and ``python manage.py migrate oppia.quiz`` to apply any database updates