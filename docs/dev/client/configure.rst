Configuring your own version of the app
===========================================

Assuming you have set up and installed you own OppiaMobile server, clearly 
you'll want your users to connect to this by default.

The core OppiaMobile android app is configured to point to our demonstration 
server (http://demo.oppia-mobile.org). To have your version of the app 
automatically point to your server:

* Open the ``/res/values/strings.xml`` file
* Change the ``prefServerDefault`` string to be the url to your server