OppiaMobile Server Change Log for v0.9.x
==========================================

To see the upcoming feature developments and bug fixes, please refer to the `monthly milestones on GitHub <https://github.com/DigitalCampus/django-oppia/milestones>`_


.. _serverv0.9.12:

v0.9.12 - Released 22 Jan 2018
--------------------------------

* 411: Add new logo - https://github.com/DigitalCampus/django-oppia/issues/411
* 422: Check user course summaries - https://github.com/DigitalCampus/django-oppia/issues/422
* 415: add defusedxml==0.5.0 as requirement - https://github.com/DigitalCampus/django-oppia/issues/415
* 412: Update docs to reflect new question type functionality - https://github.com/DigitalCampus/django-oppia/issues/412
* 410: Update docs for creating a new version/Implementation of Oppia app - https://github.com/DigitalCampus/django-oppia/issues/410
* 425: Review and  update the upgrade docs - https://github.com/DigitalCampus/django-oppia/issues/425
* 437: Redirect "link to open activity in app" to the preview page - https://github.com/DigitalCampus/django-oppia/issues/437

.. _serverv0.9.11:

v0.9.11 - Released 29 Sept 2017
--------------------------------

* 368: Move settings model to top level - https://github.com/DigitalCampus/django-oppia/issues/368
* 406: Update to using django 1.8.17 (more recent version of 1.8 LTS) - https://github.com/DigitalCampus/django-oppia/issues/406
* Hotfix to solve problem when there is more than one quiz with the same digest - https://github.com/DigitalCampus/django-oppia/pull/420

.. _serverv0.9.10:

v0.9.10 - Released 22 Jun 2017
--------------------------------

* 416: temp upload directory not getting deleted correctly - https://github.com/DigitalCampus/django-oppia/issues/416
* Replace and scrape thoroughly HTML entities in the course XML

.. _serverv0.9.9:

v0.9.9 - Released 7 Apr 2017
--------------------------------

* hotfix: multiple quizzes returned - https://github.com/DigitalCampus/django-oppia/pull/408 and https://github.com/DigitalCampus/django-oppia/pull/409


.. _serverv0.9.8:

v0.9.8 - Released 5 Jan 2017
--------------------------------

* 349: Management command for cleaning up old data - http://github.com/DigitalCampus/django-oppia/issues/issue/349
* 219: Add better error messaging/reporting when upload fails - http://github.com/DigitalCampus/django-oppia/issues/issue/219
* 22: Add unit tests for BadgesResource - http://github.com/DigitalCampus/django-oppia/issues/issue/22
* 25: Add unit tests for CourseResource - http://github.com/DigitalCampus/django-oppia/issues/issue/25
* 26: Add unit tests for PointsResource - http://github.com/DigitalCampus/django-oppia/issues/issue/26
* 47: Add unit test for checking registration done through web form - http://github.com/DigitalCampus/django-oppia/issues/issue/47
* 359: Add unit tests for permissions - http://github.com/DigitalCampus/django-oppia/issues/issue/359
* 227: Check that the direct course upload via Moodle will reject any files larger than specified for the server - http://github.com/DigitalCampus/django-oppia/issues/issue/227
* 310: Change quiz export method - https://github.com/DigitalCampus/django-oppia/issues/310
* 394: Management command to clean uploads dir - https://github.com/DigitalCampus/django-oppia/issues/394

.. _serverv0.9.7:

v0.9.7 - Released 20 Sept 2016
--------------------------------

* 370: New points summary is ignoring non-course points - http://github.com/DigitalCampus/django-oppia/issues/issue/370
* 365: Docs add info about permissions for publishing courses and app - http://github.com/DigitalCampus/django-oppia/issues/issue/365
* 367: API course list - show user who published course - http://github.com/DigitalCampus/django-oppia/issues/issue/367
* 310: Change quiz export method - http://github.com/DigitalCampus/django-oppia/issues/issue/310
* 262: On course upload indicate if the digests have changed - http://github.com/DigitalCampus/django-oppia/issues/issue/262

.. _serverv0.9.6:

v0.9.6 - Released 26 Jul 2016
--------------------------------

* 177: Add previous/next options for courses - now getting to be long list - http://github.com/DigitalCampus/django-oppia/issues/issue/177
* 306: Display course progress graphically - http://github.com/DigitalCampus/django-oppia/issues/issue/306
* 327: On courses list page add option to filter by draft and archived courses - http://github.com/DigitalCampus/django-oppia/issues/issue/327
* 337: On courses list page add option to edit the course - http://github.com/DigitalCampus/django-oppia/issues/issue/337
* 371: Some users having very inflated number of points - http://github.com/DigitalCampus/django-oppia/issues/issue/371
* 372: Add new summary tables to django admin pages - http://github.com/DigitalCampus/django-oppia/issues/issue/372
* 373: Summary cron - oppia.models.DoesNotExist: Tracker matching query does not exist - http://github.com/DigitalCampus/django-oppia/issues/issue/373

.. _serverv0.9.5:

v0.9.5 - Released 8 Jul 2016
--------------------------------

.. note::
 	This release implements significant performance improvements on the server dashboard and has been achieved by 
 	caching a lot of the data needed to generate the activity graphs and progress. After updating to this version, you 
 	will need to check that a regular cron task is set up to run the `oppia/summary/cron.py` script. It may take some 
 	time (10 mins+) to run the first time if you have a lot of existing data, but after that each time the cron task is 
 	run should take only a few seconds. If the cron task is not set up to run, then you will not see any activity in the 
 	dashboard graphs.

* 304: Deprecation warning for Django 1.8 - http://github.com/DigitalCampus/django-oppia/issues/issue/304
* 269: Add display of media/videos to the course and user views - http://github.com/DigitalCampus/django-oppia/issues/issue/269
* 331: Cron task gives error if `uploads/temp` dir doesn't exist - http://github.com/DigitalCampus/django-oppia/issues/issue/331
* 323: Performance issues when loading dashboard with a lot of data - http://github.com/DigitalCampus/django-oppia/issues/issue/323
* 243: Dashboard homepage and course pages very slow - http://github.com/DigitalCampus/django-oppia/issues/issue/243

.. _serverv0.9.4:

v0.9.4 - Released 2 May 2016
--------------------------------

* 289: Add default report for no badges (course completion rates) - http://github.com/DigitalCampus/django-oppia/issues/issue/289
* 273: Refactor UserProfile model - http://github.com/DigitalCampus/django-oppia/issues/issue/273
* 314: After logout, then logging in again the page redirects to logout again - http://github.com/DigitalCampus/django-oppia/issues/issue/314
* 276: Add content development training course to docs - http://github.com/DigitalCampus/django-oppia/issues/issue/276
* 313: Add architecture/workflow to docs - http://github.com/DigitalCampus/django-oppia/issues/issue/313
* 305: Refactor usage of staticfiles - using django 1.8 method - http://github.com/DigitalCampus/django-oppia/issues/issue/305
* 339: Quiz matching query does not exist - http://github.com/DigitalCampus/django-oppia/issues/issue/339
* 303: Add option to reorder the columns in the tables - http://github.com/DigitalCampus/django-oppia/issues/issue/303
* 284: Facility to export list of users for loading into the app - http://github.com/DigitalCampus/django-oppia/issues/issue/284
* 207: Fix issue where activities may not have descriptions entered - http://github.com/DigitalCampus/django-oppia/issues/issue/207
* 280: Improved error checking for video embed helper - http://github.com/DigitalCampus/django-oppia/issues/issue/280
* 286: Implement the server side part of device admin API into the core - http://github.com/DigitalCampus/django-oppia/issues/issue/286
* 284: Facility to export list of users for loading into the app - http://github.com/DigitalCampus/django-oppia/issues/issue/284
* 300: Improve interface for managing cohorts - http://github.com/DigitalCampus/django-oppia/issues/issue/300
* 302: Add option to search for users to get their activity - http://github.com/DigitalCampus/django-oppia/issues/issue/302

.. note::
 	Make sure that django.contrib.staticfiles is included in your INSTALLED_APPS setting (for issue #305 above)

.. _serverv0.9.3:

v0.9.3 - Released 22 Feb 2016
--------------------------------

* 287: Separate out the local_settings for dev, staging and live - http://github.com/DigitalCampus/django-oppia/issues/issue/287
* 290: Add local settings option for the course badges criteria - http://github.com/DigitalCampus/django-oppia/issues/issue/290
* 270: Add documentation about the Device Admin API - http://github.com/DigitalCampus/django-oppia/issues/issue/270
* 283: Error in video embed helper (list index out of range) - http://github.com/DigitalCampus/django-oppia/issues/issue/283
* 294: Add logging of dashboard access - http://github.com/DigitalCampus/django-oppia/issues/issue/294
* 298: Allow searching for courses in Django Admin - http://github.com/DigitalCampus/django-oppia/issues/issue/298
* 299: 'Add cohort' button styling - http://github.com/DigitalCampus/django-oppia/issues/issue/299
* 288: Allow downloading of raw data from the summary overview page - http://github.com/DigitalCampus/django-oppia/issues/issue/288
* 274: Fix issue with date picker not displaying the date - http://github.com/DigitalCampus/django-oppia/issues/issue/274
* HOTFIX (1 Mar 2016): 316: One user has 124 badges - http://github.com/DigitalCampus/django-oppia/issues/issue/316

.. _serverv0.9.2:

v0.9.2 - Released 10 Dec 2015
--------------------------------

* 271: Add documentation for the training plans - http://github.com/DigitalCampus/django-oppia/issues/issue/271
* 277: Add page in the server to allow easier generation of video embed code - http://github.com/DigitalCampus/django-oppia/issues/issue/277


.. _serverv0.9.1:

v0.9.1 - Released 23 Oct 2015
--------------------------------

* 265: Write docs on points and badging - http://github.com/DigitalCampus/django-oppia/issues/issue/265
* 267: Updating for Django 1.8 - http://github.com/DigitalCampus/django-oppia/issues/issue/267
* 266: Update home page (not logged in) and about page - http://github.com/DigitalCampus/django-oppia/issues/issue/266

.. _serverv0.9.0:

v0.9.0 - Released 11 Oct 2015
--------------------------------

* 250: Add docs about groups and permissions - https://github.com/DigitalCampus/django-oppia/issues/issue/250
* 255: Don't show upload option in main menu if no permissions - https://github.com/DigitalCampus/django-oppia/issues/issue/255
* 254: Update and redesign the user activity page on the dashboard - https://github.com/DigitalCampus/django-oppia/issues/issue/254
* 260: RelatedObjectDoesNotExist error if user has no profile record - https://github.com/DigitalCampus/django-oppia/issues/issue/260
* 261: Add link to django admin in menu (for superusers) - https://github.com/DigitalCampus/django-oppia/issues/issue/261
* 264: Allow editing of profiles by staff users - https://github.com/DigitalCampus/django-oppia/issues/issue/264
* 239: Check why getting a lot of duplicate tracker items in the table - https://github.com/DigitalCampus/django-oppia/issues/issue/239
* 208: On user page show graph of activity - https://github.com/DigitalCampus/django-oppia/issues/issue/208
* 253: Review permissions on dashboard to make sure they're sensible - https://github.com/DigitalCampus/django-oppia/issues/issue/253


