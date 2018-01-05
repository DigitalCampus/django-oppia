Server Settings
===============

These are the settings that you may want to alter to adapt to your OppiaMobile 
installation.

To edit these settings you will need to edit the ``local_settings_xxx.py`` file, and
for them to take effect you will need to restart your web server.
 
OPPIA_POINTS
-------------

Default: 
	``'REGISTER':100,                             # given when user first registers
        'QUIZ_ATTEMPT_OWNER':5,                     # given to the quiz owner when another user attempts their quiz 
        'QUIZ_FIRST_ATTEMPT':20,                    # for the first attempt at a quiz 
        'QUIZ_ATTEMPT':10,                          # for any subsequent attempts at a quiz 
        'QUIZ_FIRST_ATTEMPT_THRESHOLD':100,         # Threshold for getting bonus points for first attempt at quiz (must be 0-100)
        'QUIZ_FIRST_ATTEMPT_BONUS':50,              # Bonus points for getting over the threshold on first attempt at quiz 
        'QUIZ_CREATED':200,                         # for creating a quiz
        'ACTIVITY_COMPLETED':10,                    # for completing an activity
        'MEDIA_STARTED':20,                         # for starting media
        'MEDIA_PLAYING_INTERVAL':30,                # interval in seconds for which points are given
        'MEDIA_PLAYING_POINTS_PER_INTERVAL':5,      # no points per interval media is playing
        'MEDIA_MAX_POINTS':200,                     # the maximum number of points available for any single media play
        'COURSE_DOWNLOADED':50, 
      ``


OPPIA_METADATA
---------------

The defines the metadata info that is sent back from the app.

OPPIA_ALLOW_SELF_REGISTRATION
-----------------------------

Default: ``True``

This settings determines whether users are able to self register (i.e. anyone 
can create an account) on the server. Set this to ``False`` to prevent just 
anyone registering on your server - you will need to create their accounts 
yourself instead using the standard Django user management.


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

* BADGE_AWARD_METHOD_ALL_ACTIVITIES (default) - all activities in the course must be completed, and all quizzes passed
* BADGE_AWARD_METHOD_FINAL_QUIZ - only need to pass the final quiz
* BADGE_AWARD_METHOD_ALL_QUIZZES - all the quizzes in the course must be passed


OPPIA_GOOGLE_ANALYTICS_ENABLED
------------------------------

Default: ``True``

Whether or not to turn on Google Analytics tracking for your Oppia server.

OPPIA_GOOGLE_ANALYTICS_CODE
---------------------------

Your Google Analytics tracking code - only used if OPPIA_GOOGLE_ANALYTICS_CODE
is set to True.

OPPIA_GOOGLE_ANALYTICS_DOMAIN
-----------------------------

Your Google Analytics domain name - only used if ``OPPIA_GOOGLE_ANALYTICS_CODE`` is 
set to ``True``.


OPPIA_MAX_UPLOAD_SIZE
---------------------

Default: 5242880 (5Mb)

This is the maximum file course file size that can be uploaded (in bytes). This
is to prevent users uploading very large files - for example if they haven't 
appropriately resized images, or included video or other media files. Large 
course upload files may cause issues for end users (particularly those with slow
internet connections) when trying to install the course on their phone.

If you define a `MAX_UPLOAD_SIZE` property in the SettingProperties table (under the Django admin),
that value will take precedence from the one defined in the `_settings.py` file


OPPIA_VIDEO_FILE_TYPES
-----------------------

List of the video file MIME types that will be accepted for upload to the server.

OPPIA_AUDIO_FILE_TYPES
------------------------------

List of the audio file MIME types that will be accepted for upload to the server.

OPPIA_EXPORT_LOCAL_MINVERSION
--------------------------------

Default: 2017011400

The minimum version no of the Moodle - Oppia export block to process the quizzes locally on the server.


API_LIMIT_PER_PAGE
--------------------

Default: 0

Defines how many results will be returned per page in the API. When set to 0, all results will be returned.


DEVICE_ADMIN_ENABLED
-----------------------

Default: True

Defines if the Google Device Admin functionality is enabled. Note that if it is enabled here and in the Oppia app, then 
extra information is required in the app to ensure users are aware of these permissions. If this info is not provided in 
the app, then it may get removed from Google Play.

