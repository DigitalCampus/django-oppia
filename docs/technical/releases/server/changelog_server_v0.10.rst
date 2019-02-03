OppiaMobile Server Change Log for v0.10.x
==========================================

.. _serverv0.10.1:

v0.10.1 - Released 23 Nov 2018
--------------------------------

.. warning:: 
	Run `pip install -r django-oppia/requirements.txt` after upgrading to this version, since new packages
	and an updated version of Django is used.
	
	Update calls to the cartodb_update and ip2location functions to use management commands instead

Key updates:

* updated version of Django, to 1.11.11 LTS
* improvements to media uploading
* support for points assigned offline by the app
* code improvements and bug fixes

Issue list:

* 453: Upgrade to Django 1.11.11 - https://github.com/DigitalCampus/django-oppia/issues/453
* 443: Check and prevent duplicate trackers being submitted (based on UUID) - https://github.com/DigitalCampus/django-oppia/issues/443
* 452: Check quizresponses for duplicates - https://github.com/DigitalCampus/django-oppia/issues/452
* 442: Option to upload the downloaded tracker files - https://github.com/DigitalCampus/django-oppia/issues/442
* 454: On media upload, error not showing if libav-tools not installed - https://github.com/DigitalCampus/django-oppia/issues/454
* 428: UploadMedia - finding, displaying & downloading media - https://github.com/DigitalCampus/django-oppia/issues/428
* 426: UploadedMedia - show embed code - https://github.com/DigitalCampus/django-oppia/issues/426
* 448: Update customisation documentation - https://github.com/DigitalCampus/django-oppia/issues/448
* 427: UploadMedia - process to generate sample images - https://github.com/DigitalCampus/django-oppia/issues/427
* 460: Upload media - display sample images and allow selection of default - https://github.com/DigitalCampus/django-oppia/issues/460
* 467: Add option to highlight if dev server - https://github.com/DigitalCampus/django-oppia/issues/467
* 465: Activity upload - show message if user is not found - https://github.com/DigitalCampus/django-oppia/issues/465
* 445: Add points info from module.xml into db when course uploaded - https://github.com/DigitalCampus/django-oppia/issues/445
* 447: Update tracker API to use points submitted from app - https://github.com/DigitalCampus/django-oppia/issues/447
* 470: Add points and events into tracker and quiz attempt xml files - https://github.com/DigitalCampus/django-oppia/issues/470
* 472: sorl-thumbnail is listed as a requirement but not included as a project dependency on setup.py - https://github.com/DigitalCampus/django-oppia/issues/472
* 474: Broken links on documentation (installation page) - https://github.com/DigitalCampus/django-oppia/issues/474
* 478: Search for <media> element can fail when importing course - https://github.com/DigitalCampus/django-oppia/issues/478
* 480: Remove code related to scheduling - https://github.com/DigitalCampus/django-oppia/issues/480
* 481: Remove code related to messaging - https://github.com/DigitalCampus/django-oppia/issues/481
* 459: Clean up utils dir - https://github.com/DigitalCampus/django-oppia/issues/459
* 498: Search users page not functioning... - https://github.com/DigitalCampus/django-oppia/issues/498
* 449: Option to export leaderboard data - https://github.com/DigitalCampus/django-oppia/issues/449
* 482: Remove code related to monitoring page - https://github.com/DigitalCampus/django-oppia/issues/482

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