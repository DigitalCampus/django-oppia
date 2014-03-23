Change Log for v0.1.x
======================

v0.1.40
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/109 - error uploading courses
* Update documentation for AWS machine image

v0.1.39
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/103
* Use updated versions of Django, TastyPie and South

v0.1.38
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/98 - use XSD for validating uploaded packages
* Fix: https://github.com/DigitalCampus/django-oppia/issues/91 - don't return full quiz object
* Fix: https://github.com/DigitalCampus/django-oppia/issues/89 - exclude description questions from display
* Fix: https://github.com/DigitalCampus/django-oppia/issues/57 - order quizzes by section/activity

v0.1.37
--------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/76 - fix mismatch between graphs/leaderboard/activity detail
* Fix: https://github.com/DigitalCampus/django-oppia/issues/84 - new local settings
* Fix: https://github.com/DigitalCampus/django-oppia/issues/85 - add resources to activity graph

v0.1.35
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/77 - return is_draft with course resources
* Fix: https://github.com/DigitalCampus/django-oppia/issues/60 - fix Tag API so only returns course relevant for user

v0.1.34
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/72 - Tracker API error when more than one media with same digest

v0.1.33
-------
* Really fix: https://github.com/DigitalCampus/django-oppia/issues/68 - add fixtures to PyPi package

v0.1.32
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/71 - adding tracker data
* Fix: https://github.com/DigitalCampus/django-oppia/issues/68 - add fixtures to PyPi package

v0.1.31
-------
* Upgrade to use more recent version of TastyPie (0.9.16)
* Fix: https://github.com/DigitalCampus/django-oppia/issues/67

v0.1.30
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/49
* Fix: https://github.com/DigitalCampus/django-oppia/issues/63

v0.1.29
-------
* Handle adding baseline quizzes/activities: https://github.com/DigitalCampus/django-oppia/issues/56

v0.1.28
-------
* Bug fix returning metadata in Tracker API

v0.1.26
-------
* New local setting to allow only staff status to upload courses: https://github.com/DigitalCampus/django-oppia/issues/40
* Points for watching media now determined by how many mins of the video has been watched: https://github.com/DigitalCampus/django-oppia/issues/6
* New local setting to allow only points to be turned on/off on the server: https://github.com/DigitalCampus/django-oppia/issues/50
* New local settings to determine which metadata should be collected from the phone: https://github.com/DigitalCampus/django-oppia/issues/55

v0.1.23
-------
* Fix cohort editing form: https://github.com/DigitalCampus/django-oppia/issues/54
* In cohort admin page show participants in inline tabular form

v0.1.22
-------
* Show recent activity as a graph rather than just numbers for today and last week
* Begin to add teacher monitoring pages

v0.1.21
-------
* Add option to turn self registration on or off: https://github.com/DigitalCampus/django-oppia/issues/2
* Add option for added Google Analytics: https://github.com/DigitalCampus/django-oppia/issues/1

v0.1.20
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/46

v0.1.19
-------
* Added script for scanning dir of video files to create the tags: https://github.com/DigitalCampus/django-oppia/issues/44
* Also added auto creation of images for video files: https://github.com/DigitalCampus/django-oppia/issues/45

v0.1.18
-------
* Fix awarding points with badges: https://github.com/DigitalCampus/django-oppia/issues/41
* Fix: https://github.com/DigitalCampus/django-oppia/issues/13
* Add version number to footer
* Add views for quiz results

v0.1.17
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/18
* Added unit tests for QuizAttempt https://github.com/DigitalCampus/django-oppia/issues/39
* Fix: https://github.com/DigitalCampus/django-oppia/issues/42

v0.1.16
-------
* Add default badges data
* Fix error in running cron script and awarding badges

v0.1.15
-------
* Begun to add unit tests
* More info on courses page about current activity

v0.1.14
-------
* Fix: https://github.com/DigitalCampus/django-oppia/issues/19

v0.1.13
-------
* Add a max upload file size (https://github.com/DigitalCampus/django-oppia/issues/8) - this prevents users uploading large course files which may make it difficult for end users to download on slow connections
* Updated mobile scorecard page
* Added extra info on Django admin pages (https://github.com/DigitalCampus/django-oppia/issues/14)

v0.1.12
-------
* Initial release (all previous versions were for alpha testing)