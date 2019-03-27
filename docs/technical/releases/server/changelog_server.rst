OppiaMobile Server Change Log
================================

.. _serverv0.11.0:

v0.11.0 - Released 20 Mar 2019
--------------------------------

.. toctree::
   :maxdepth: 1

   upgrading/to_0_11_0

	
Key updates:

* Upgrading to Django 1.11.20
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
* 525: Remove development_server setting and use debug instead - https://github.com/DigitalCampus/django-oppia/issues/525
* 530: Move cron and cronsummary tasks to be under the oppiamobile directory? - https://github.com/DigitalCampus/django-oppia/issues/530
* 364: Logging when cron was last run - https://github.com/DigitalCampus/django-oppia/issues/364
* 375: Implement cron lock - https://github.com/DigitalCampus/django-oppia/issues/375
* 565: Copy the OPPIA_ALLOW_SELF_REGISTRATION setting.py into SettingProperties - https://github.com/DigitalCampus/django-oppia/issues/565
* 558: Add upgrade docs to v0.11.0 - https://github.com/DigitalCampus/django-oppia/issues/558
* 297: Docs for export process from Moodle to Oppia - https://github.com/DigitalCampus/django-oppia/issues/297
* 561: Add app settings to docs - https://github.com/DigitalCampus/django-oppia/issues/561
* 496: Improve how email templates are handled - https://github.com/DigitalCampus/django-oppia/issues/496
* 563: Remove oppia/cron.py and move it to the management command oppiacron.py - https://github.com/DigitalCampus/django-oppia/issues/563
* 576: Use the db settings for storing/editing the ip2location and cartodb_update usernames, api_keys - https://github.com/DigitalCampus/django-oppia/issues/576
* 533: Styling with BootStrap 4 - https://github.com/DigitalCampus/django-oppia/issues/533
* 555: Cohort add/edit form doesn't show the list of available teachers/students - https://github.com/DigitalCampus/django-oppia/issues/555
* 575: TypeError: 'Tracker' object has no attribute '__getitem__' - https://github.com/DigitalCampus/django-oppia/issues/575
* 554: Cohort add/edit form has some layout issues - https://github.com/DigitalCampus/django-oppia/issues/554
* 573:  Update/review docs for how the bluetooth transfer works - https://github.com/DigitalCampus/django-oppia/issues/573
* 574: Update/review docs for how the activity log transfer works - https://github.com/DigitalCampus/django-oppia/issues/574
* 579: Media viewed not being displayed correctly - https://github.com/DigitalCampus/django-oppia/issues/579
* 580: Course download points being left out - https://github.com/DigitalCampus/django-oppia/issues/580
* 581: Quiz attempt points being added twice - https://github.com/DigitalCampus/django-oppia/issues/581
* 590: Quiz points added twice - from tests - https://github.com/DigitalCampus/django-oppia/issues/590
* 592: Move to Django 1.11.20 on v0.11.0 branch & master - https://github.com/DigitalCampus/django-oppia/issues/592
* 570: Make sure use of COURSE_UPLOAD_DIR always uses os.path.join() - https://github.com/DigitalCampus/django-oppia/issues/570

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
