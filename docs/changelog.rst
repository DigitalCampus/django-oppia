Change Log
============

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