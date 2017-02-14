OppiaMobile Android App Install FAQs
=======================================

If you are having trouble installing the app and logging in/registering, there are a few checks that you can do. These 
are likely to be most relevant those trying to set up the app on older Android phones, or when you are on a very slow 
connection.

Check for system updates
-------------------------

First item to check is that the phone has all the available system updates installed. It is good practice to keep the 
phones up to date with system updates, for bugs and security issues. To check if any updates are available, go to (from 
the main Android settings): Settings -> About Phone -> System Updates. The exact sequence to check for updates may vary 
slightly on different versions of Android.

Longer Connection and Response Timeout
----------------------------------------

If you are on a particularly slow connection (for example when trying to register or log in the OppiaMobile app), the 
connection may timeout before a response has been received.

In the Oppia app settings, you can increase the 'connection timeout' and 'response timeout'. The default is 60000 
(milliseconds, so one minute), so try to increase to 120000 (two minutes).

Check Phone Date Setting
--------------------------

Check that the phone system date is set to the correct date. When connecting to an Oppia server using a secure 
connection (SSL, https), the server certificates are valid for a particular date range. If the phone date is incorrect, 
and falls outside the security certificate validity period, then the phone will refuse the connection.

Check Server Name
--------------------

Check that the server name (under the Oppia settings) is correct. The app should automatically add a trailing '/' to the 
server name if one hasn't been entered already. By default most OppiaMobile implementations will try to use an SSL 
connection, however some older versions of Android may not have the trusted certificate authority certificates 
installed, in which case you may need to fall back to using a non-SSL connection, so replace 'https://...' with 
'http://...' at the beginning of the server name.
