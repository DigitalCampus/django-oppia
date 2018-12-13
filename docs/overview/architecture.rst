OppiaMobile Platform Architecture and Components
====================================================

Architecture and Workflow
---------------------------

.. image:: images/oppia-platform-architecture.png

#. Courses are authored in Moodle.
#. When the course is exported from Moodle, the quizzes are automatically exported to the OppiaMobile server.
#. After export from Moodle, the module zip package can be downloaded and then uploaded into the learning modules app 
   in the OppiaMobile server. The reason for leaving this as a manual upload (rather than automatically published) is to 
   allow content authors the option to test out the content on their devices before it is pushed out as an automatic 
   update to learners.
#. Our OppiaMobile server provides the core of the server side, dealing with all user accounts, modules, quiz result 
   submission and tracking activity.
#. When users install the OppiaMobile Android app, their accounts are created on the OppiaMobile server. All quiz 
   attempts and results are submitted from the OppiaMobile Android app to the OppiaMobile engine (when the user has an 
   internet connection available).
#. All learning modules are downloaded from the OppiaMobile server and all tracking activity by the user (pages viewed, 
   videos watched and quiz attempts) is submitted to the OppiaMobile server by the OppiaMobile Android app. The
   OppiaMobile server also deals with all the points and badges awarded.
#. The OppiaMobile Android app delivers the learning content on the users phone.
#. Media and video content can be hosted on any website, providing it allows a direct download of the video file. 
   Currently all the media content is hosted in a static directory structure on our demo OppiaMobile website 
   (http://downloads.digital-campus.org/media/) – but this is only for convenience, rather than a requirement.
#. The OppiaMobile Android app can download the videos from the media hosting (if a wifi connection is available). 
   Alternatively the media files may be directly copied onto the phone SD card.

    
Components Source Code
-------------------------------

OppiaMobile Android App
^^^^^^^^^^^^^^^^^^^^^^^^

The app is compatible with Android API level 14+ (i.e. Android version 4+).

* Source code: https://github.com/DigitalCampus/oppia-mobile-android
* Bug/issue tracker: https://github.com/DigitalCampus/oppia-mobile-android/issues

OppiaMobile Server
^^^^^^^^^^^^^^^^^^^

Provides the core server-side, using the Django framework.

* Source code: https://github.com/DigitalCampus/django-oppia
* Bug/issue tracker: https://github.com/DigitalCampus/django-oppia/issues

OppiaMobile Moodle block
^^^^^^^^^^^^^^^^^^^^^^^^^^

A Moodle block (script) to export the course from Moodle into the right format for installing in the OppiaMobile Android 
app. 

* Source code: https://github.com/DigitalCampus/moodle-block_oppia_mobile_export
* Bug/issue tracker: https://github.com/DigitalCampus/moodle-block_oppia_mobile_export/issues
