Local Settings
===============

These are the settings that you may want to alter to adapt to your OppiaMobile 
installation.

To edit these settings you will need to edit the ``local_settings.py`` file, and
for them to take effect you will need to restart your web server.
 

OPPIA_ALLOW_SELF_REGISTRATION
-----------------------------

Default: ``True``

This settings determines whether users are able to self register (i.e. anyone 
can create an account) on the server. Set this to ``False`` to prevent just 
anyone registering on your server - you will need to create their accounts 
yourself instead using the standard Django user management.

OPPIA_COURSE_OWNERS_EARN_POINTS
--------------------------------

Default: ``False``

Determines if the user who uploaded the course will earn points or not for 
activity within this course. This setting is ignored if ``OPPIA_POINTS_ENABLED``
is ``False``.


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


OPPIA_POINTS_ENABLED
-----------------------

Default: ``True``

This setting determines whether the points system is enabled for this server. It 
currently just hides the points from display on the mobile app.

OPPIA_TEACHERS_EARN_POINTS
--------------------------------

Default: ``False``

Determines if teachers on the course will earn points or not for activity within
this course. This setting is ignored if ``OPPIA_POINTS_ENABLED`` is ``False``.

OPPIA_SHOW_GRAVATARS
--------------------------------

Default: ``True``

Determines if a users gravatar will appear next to their name (in the 
leaderboard/activity reports etc)

OPPIA_STAFF_EARN_POINTS
-----------------------

Default: ``False``

Determines if users with the is_staff permission will earn points or not. This 
setting is ignored if ``OPPIA_POINTS_ENABLED`` is ``False``.

OPPIA_STAFF_ONLY_UPLOAD
-----------------------

Default: ``True``

This setting determines whether only users with the Django is_staff status are 
allowed to upload new courses. When this setting is ``True``, only users with 
the is_staff status are able to upload courses. If this setting is set to 
``False``, any registered user on the server is able to upload courses.
