OppiaMobile Server Change Log
================================

.. _serverv0.11.0:

v0.11.0 - not yet released
--------------------------------

.. note:: 
	In this release the project structure has changed, so you will need to make 
	changes to your OppiaMobile server set up, see :doc:`upgrading/to_0_11_0`

	
Key updates:

* Upgrading to Django 1.11.18
* Restructuring of project to match Django best practice
* Extra automated tests
* Improved documentation structure and updates

Issue list:

* 486: Refactor django project structure - https://github.com/DigitalCampus/django-oppia/issues/486
* 495: Use CDN versions of js libraries rather than local copies - https://github.com/DigitalCampus/django-oppia/issues/495
* 492: Update leaderboard pagination display to match the courses - https://github.com/DigitalCampus/django-oppia/issues/492
* 389: Implement "Open activity in app" functionality - https://github.com/DigitalCampus/django-oppia/issues/389
* 490: Use LESS/SASS for better frontend development - https://github.com/DigitalCampus/django-oppia/issues/490
* 488: Update to use Bootstrap 4 - https://github.com/DigitalCampus/django-oppia/issues/488
* 519: Update to Django 1.11.15 - https://github.com/DigitalCampus/django-oppia/issues/519
* 521: Add a 'contributing.md' file - https://github.com/DigitalCampus/django-oppia/issues/521
* 523: Remove the 'mobile' & 'preview' directories - https://github.com/DigitalCampus/django-oppia/issues/523
* 534: Error on publishing course, due to project restructuring - https://github.com/DigitalCampus/django-oppia/issues/534
* 504: In Ubuntu 18.04 avprobe is replaced with ffprobe - https://github.com/DigitalCampus/django-oppia/issues/504
* 536: Update to Django 1.11.18 - https://github.com/DigitalCampus/django-oppia/issues/536
* 535: Add tests for publishing courses and media files using the API - https://github.com/DigitalCampus/django-oppia/issues/535
* 532: Database migration fails on 0012_fix_future_tracker_dates.py - https://github.com/DigitalCampus/django-oppia/issues/532
* 537: Add tests for the uploading media (via the webform) - https://github.com/DigitalCampus/django-oppia/issues/537
* 543: Add tests for editing user profile (via form) - https://github.com/DigitalCampus/django-oppia/issues/543
* 544: SonarQube - complexity of profile/views.py edit function - https://github.com/DigitalCampus/django-oppia/issues/544
* 553: SonarQube - complexity of viz/views.py summary_view function - https://github.com/DigitalCampus/django-oppia/issues/553
* 516: Update docs for installing - with the new project structure - https://github.com/DigitalCampus/django-oppia/issues/516
* 505: Investigate options for less reliance on specific command line tools - https://github.com/DigitalCampus/django-oppia/issues/505
* 538: Update platform architecture/workflow docs - https://github.com/DigitalCampus/django-oppia/issues/538
* 489: Restructure documentation - https://github.com/DigitalCampus/django-oppia/issues/489
* 477: MIDDLEWARE_CLASSES deprecation during installation - https://github.com/DigitalCampus/django-oppia/issues/477
* 494: Badges page is not linked to from anywhere? - https://github.com/DigitalCampus/django-oppia/issues/494
* 559: Add tests for profile urls - https://github.com/DigitalCampus/django-oppia/issues/559
* 560: Add tests and data for viz models and functions - https://github.com/DigitalCampus/django-oppia/issues/560
* 557: Unusual start date on the summary overview - https://github.com/DigitalCampus/django-oppia/issues/557
* 526: Review and update server settings page - https://github.com/DigitalCampus/django-oppia/issues/526

Upgrade Notes
----------------

.. toctree::
   :maxdepth: 1

   upgrading/to_0_11_0

Previous Versions
------------------

.. toctree::
   :maxdepth: 2
   
   changelog_server_v0.10
   changelog_server_v0.9
   changelog_server_v0.8
   changelog_server_v0.7
   changelog_server_v0.6
   changelog_server_v0.5
   changelog_server_v0.4
   changelog_server_v0.3
   changelog_server_v0.2
   changelog_server_v0.1
