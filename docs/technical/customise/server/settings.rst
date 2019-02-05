Server Settings
===============

These are the settings that you may want to alter to adapt to your OppiaMobile 
installation.

To edit these settings you will need to edit your ``/oppiamobile/settings_secret.py`` file, and
for them to take effect you will need to restart your web server.
 
 
COURSE_UPLOAD_DIR
------------------

Default `ROOT_DIR +'/upload'`

This is the path to where uploaded course will be saved.


OPPIA_METADATA
---------------

Default:

::

	{
	    'NETWORK': True,  
	    'DEVICE_ID': True,
	    'SIM_SERIAL': True,
	    'WIFI_ON': True,
	    'NETWORK_CONNECTED': True,
	    'BATTERY_LEVEL': True,
	    'GPS': False,
	}

The defines the metadata info that is sent back from the app.

OPPIA_ALLOW_SELF_REGISTRATION
-----------------------------

Default: ``True``

This settings determines whether users are able to self register (i.e. anyone 
can create an account) on the server. Set this to ``False`` to prevent just 
anyone registering on your server - you will need to create their accounts 
yourself instead using the standard Django user management.

If you define a `OPPIA_ALLOW_SELF_REGISTRATION` property in the SettingProperties table (under the Django admin),
that value will take precedence from the one defined in the ``settings_secret.py`` file


OPPIA_SHOW_GRAVATARS
--------------------------------

Default: ``True``

Determines if a users gravatar will appear next to their name (in the 
leaderboard/activity reports etc)


OPPIA_STAFF_ONLY_UPLOAD
-----------------------

Default: ``True``

This setting determines whether only users with the Django is_staff status are 
allowed to upload new courses. When this setting is ``True``, only users with 
the is_staff status are able to upload courses. If this setting is set to 
``False``, any registered user on the server is able to upload courses.

You can also give upload permissions to individual users (whatever their staff 
status) by setting the can_upload option to true in their user profile.


OPPIA_POINTS_ENABLED
-----------------------

Default: ``True``

This setting determines whether the points system is enabled for this server. It 
currently just hides the points from display on the mobile app.


OPPIA_STAFF_EARN_POINTS
-----------------------

Default: ``False``

Determines if users with the is_staff permission will earn points or not. This 
setting is ignored if ``OPPIA_POINTS_ENABLED`` is ``False``.


OPPIA_COURSE_OWNERS_EARN_POINTS
--------------------------------

Default: ``False``

Determines if the user who uploaded the course will earn points or not for 
activity within this course. This setting is ignored if ``OPPIA_POINTS_ENABLED``
is ``False``.


OPPIA_TEACHERS_EARN_POINTS
--------------------------------

Default: ``False``

Determines if teachers on the course will earn points or not for activity within
this course. This setting is ignored if ``OPPIA_POINTS_ENABLED`` is ``False``.


OPPIA_BADGES_ENABLED
----------------------

Default: ``True``

This setting determines whether the badges system is enabled for this server. It 
currently just hides the badges from display on the mobile app.

BADGE_AWARDING_METHOD
------------------------

Defines the method that is used for awarding a badge. This may be set to one of:

* ``BADGE_AWARD_METHOD_ALL_ACTIVITIES`` (default) - all activities in the course must be completed, and all quizzes passed
* ``BADGE_AWARD_METHOD_FINAL_QUIZ`` - only need to pass the final quiz
* ``BADGE_AWARD_METHOD_ALL_QUIZZES`` - all the quizzes in the course must be passed


OPPIA_GOOGLE_ANALYTICS_ENABLED
------------------------------

Default: ``True``

Whether or not to turn on Google Analytics tracking for your Oppia server.

OPPIA_GOOGLE_ANALYTICS_CODE
---------------------------

Your Google Analytics tracking code - only used if ``OPPIA_GOOGLE_ANALYTICS_CODE``
is set to ``True``.

OPPIA_GOOGLE_ANALYTICS_DOMAIN
-----------------------------

Your Google Analytics domain name - only used if ``OPPIA_GOOGLE_ANALYTICS_CODE`` is 
set to ``True``.


OPPIA_MAX_UPLOAD_SIZE
---------------------

Default: ``5242880`` (5Mb)

This is the maximum file course file size that can be uploaded (in bytes). This
is to prevent users uploading very large files - for example if they haven't 
appropriately resized images, or included video or other media files. Large 
course upload files may cause issues for end users (particularly those with slow
internet connections) when trying to install the course on their phone.

If you define a `MAX_UPLOAD_SIZE` property in the SettingProperties table (under the Django admin),
that value will take precedence from the one defined in the ``settings_secret.py`` file


OPPIA_VIDEO_FILE_TYPES
-----------------------

Default: ``("video/m4v", "video/mp4", "video/3gp", "video/3gpp")``

List of the video file MIME types that will be accepted for upload to the server.

OPPIA_AUDIO_FILE_TYPES
------------------------------

Default: ``("audio/mpeg", "audio/amr", "audio/mp3")``

List of the audio file MIME types that will be accepted for upload to the server.

OPPIA_MEDIA_IMAGE_FILE_TYPES
------------------------------

Default: ``("image/png", "image/jpeg")``

List of the media image file MIME types that will be accepted for upload to the server.


OPPIA_EXPORT_LOCAL_MINVERSION
--------------------------------

Default: ``2017011400``

The minimum version no of the Moodle - Oppia export block to process the quizzes locally on the server.


API_LIMIT_PER_PAGE
--------------------

Default: ``0``

Defines how many results will be returned per page in the API. When set to 0, all results will be returned.


DEVICE_ADMIN_ENABLED
-----------------------

Default: ``False``

Defines if the Google Device Admin functionality is enabled. Note that if it is enabled here and in the Oppia app, then 
extra information is required in the app to ensure users are aware of these permissions. If this info is not provided in 
the app, then it may get removed from Google Play.

GCM_DEVICE_MODEL
-----------------

Default: ``deviceadmin.models.UserDevice``

Only used if DEVICE_ADMIN_ENABLED is ``True``

GCM_APIKEY
-----------------

Default: ``OPPIA_GOOGLEAPIKEY``

Only used if DEVICE_ADMIN_ENABLED is ``True``


OPPIA_ANDROID_PACKAGEID 
------------------------

Default:  ``'org.digitalcampus.mobile.learning'``

Package ID for linking to the Google Play Store

OPPIA_ANDROID_ON_GOOGLE_PLAY
--------------------------------

Default: ``True`` 

If the app is not on Google Play, we rely on the core version for store links


SCREENSHOT_GENERATOR_PROGRAM
----------------------------------

Default: ``ffmpeg``


SCREENSHOT_GENERATOR_PROGRAM_PARAMS
-------------------------------------

Default:``"-i %s -r 0.02 -s %dx%d -f image2 %s/frame-%%03d.png"``

MEDIA_PROCESSOR_PROGRAM
--------------------------

Default: ``"avprobe"``

For Ubuntu 18.04 and above, you should override this in ``settings_secret.py``
to be ``"ffprobe"``

MEDIA_PROCESSOR_PROGRAM_PARAMS
----------------------------------

Default: ``""``

