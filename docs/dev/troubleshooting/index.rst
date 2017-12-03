Troubleshooting an Oppia Implementation
===========================================

This page lists some common issues, their causes and what to check to resolve them.

Course doesn't show up in the app course download list
-------------------------------------------------------

* The course is marked as archived on the Oppia server. If a course is marked as archived, then it will not appear for 
  any user in the app. Check that the course is not marked as archived on the server.
* The course is marked as draft on the Oppia server. If a course is marked as draft then only admin/staff users will be 
  able to view it in the app. Either log in to the app as an admin/staff user, or remove the draft status from the 
  course in the server.
* The course has not been given any tags when being published. To view the course in the download courses part of the 
  app, each course must be given at least one tag when it has been published. If a course is updated and re-published, 
  then the tags must be given again (the original tags should be pre-filled in the course publishing form).


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

