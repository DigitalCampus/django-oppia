Troubleshooting OppiaMobile Server
=====================================


Activity for a user doesn't appear in the server
---------------------------------------------------

* The course has been updated. When a course is updated the unique references to the activities may change and if the 
  user has the old version of the course on their device, their version may not match the course version on the server. 
  Check that the users device has the most recent version of the course.
* For server performance reasons, the data used to generate the dashboard activity graphs are cached, and are only 
  updated when the server cron task is run. On installations based on the Oppia AWS machine the cron task is 
  pre-configured to run every 15 mins, so check that this is running correctly.
* If the users device is not connected to the internet (or it is pointing at the wrong OppiaMobile server) then the 
  users activity will not be reaching the Oppia server. In the app check that the server is set correctly (in menu > 
  settings > server) and that all the users activity has been sent to the server (menu > about > activity).
* If the user is an admin or staff user, then the activity is not shown in the dashboard graphs. Similarly, if the user 
  is set up as a teacher for the course, then their course activity is not reflected in the dashboard activity graphs 
  either.
  
Unable to publish a course due to permissions issue
----------------------------------------------------
 
There are three potential issues:
 
#. The username/password used is incorrect. Check the user can log in using the same username/password into the Oppia server dashboard.
#. The user does not have permissions to upload courses on the server, see: :ref:`permission-user-upload`
#. The course was originally published by a different user, see: :ref:`permission-course-ownership` 