OppiaMobile Server Change Log
================================


.. _serverv0.10.1:

.. warning:: 
	Run `pip install -r django-oppia/requirements.txt` after upgrading to this version, since new packages
	and an updated version of Django is used.

v0.10.1 - not yet released
--------------------------------

* 453: Upgrade to Django 1.11.11 - https://github.com/DigitalCampus/django-oppia/issues/issues/453
* 443: Check and prevent duplicate trackers being submitted (based on UUID) - https://github.com/DigitalCampus/django-oppia/issues/443
* 452: Check quizresponses for duplicates - https://github.com/DigitalCampus/django-oppia/issues/452
* 442: Option to upload the downloaded tracker files - https://github.com/DigitalCampus/django-oppia/issues/442
* 454: On media upload, error not showing if libav-tools not installed - https://github.com/DigitalCampus/django-oppia/issues/454
* 428: UploadMedia - finding,displaying & downloading media - https://github.com/DigitalCampus/django-oppia/issues/428
* 426: UploadedMedia - show embed code - https://github.com/DigitalCampus/django-oppia/issues/426
* 448: Update customisation documentation - https://github.com/DigitalCampus/django-oppia/issues/448
* 427: UploadMedia - process to generate sample images - https://github.com/DigitalCampus/django-oppia/issues/427


.. _serverv0.10.0:

v0.10.0 - Released 1 Feb 2018
--------------------------------

.. warning:: 
	This release requires Django 1.11 LTS. Previous versions were targeted for Django 1.8 LTS, so an upgrade of your 
	Django will be required when updating to this version of the OppiaMobile server.

* 421: Move to django v1.11.6 - https://github.com/DigitalCampus/django-oppia/issues/421
* 415: add defusedxml==0.5.0 as requirement - https://github.com/DigitalCampus/django-oppia/issues/415	
* 400: Add docs for updating the theme on the app for custom versions - https://github.com/DigitalCampus/django-oppia/issues/400
* 399: Check documentation for creating own version of app - https://github.com/DigitalCampus/django-oppia/issues/399
* 377: Course activity on summary overview showing dates into far future - https://github.com/DigitalCampus/django-oppia/issues/377	
* 390: Document management commands (purpose & how to run etc) - https://github.com/DigitalCampus/django-oppia/issues/390
* 431: Update to use TastyPie v0.14.0 - https://github.com/DigitalCampus/django-oppia/issues/431
* 433: Device admin setting error - https://github.com/DigitalCampus/django-oppia/issues/433
* 440: Option for user to export data - https://github.com/DigitalCampus/django-oppia/issues/440
* 439: Option for user to delete their account/data completely - https://github.com/DigitalCampus/django-oppia/issues/439
* 358: Improve layout of 'unauthorised' page - https://github.com/DigitalCampus/django-oppia/issues/358

Previous Versions
------------------

.. toctree::
   :maxdepth: 2
   
   changelog_server_v0.9
   changelog_server_v0.8
   changelog_server_v0.7
   changelog_server_v0.6
   changelog_server_v0.5
   changelog_server_v0.4
   changelog_server_v0.3
   changelog_server_v0.2
   changelog_server_v0.1
