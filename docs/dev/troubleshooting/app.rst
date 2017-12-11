Troubleshooting OppiaMobile App
=====================================


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

  
Cannot install app - check for system updates
--------------------------------------------------

First item to check is that the phone has all the available system updates installed. It is good practice to keep the 
phones up to date with system updates, for bugs and security issues. To check if any updates are available, go to (from 
the main Android settings): Settings -> About Phone -> System Updates. The exact sequence to check for updates may vary 
slightly on different versions of Android.

Cannot connect to server - Longer Connection and Response Timeout
-------------------------------------------------------------------

If you are on a particularly slow connection (for example when trying to register or log in the OppiaMobile app), the 
connection may timeout before a response has been received.

In the Oppia app settings, you can increase the 'connection timeout' and 'response timeout'. The default is 60000 
(milliseconds, so one minute), so try to increase to 120000 (two minutes).

Cannot connect to server - Check Phone Date Setting
----------------------------------------------------

Check that the phone system date is set to the correct date. When connecting to an Oppia server using a secure 
connection (SSL, https), the server certificates are valid for a particular date range. If the phone date is incorrect, 
and falls outside the security certificate validity period, then the phone will refuse the connection.

Cannot connect to server - Check Server Name
------------------------------------------------

Check that the server name (under the Oppia settings) is correct. The app should automatically add a trailing '/' to the 
server name if one hasn't been entered already. By default most OppiaMobile implementations will try to use an SSL 
connection, however some older versions of Android may not have the trusted certificate authority certificates 
installed, in which case you may need to fall back to using a non-SSL connection, so replace 'https://...' with 
'http://...' at the beginning of the server name.