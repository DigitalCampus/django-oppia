OppiaMobile Android App
========================

This page describes some of the basic customisations you may want to make when
implementing your own version of the OppiaMobile learning platform. Here we 
describe some of the more common requests for basic customisations, however 
since the code is open source, you are, of course, free to make any 
customisations you like.

Prerequisites
--------------
Before being able to create your own version of the OppiaMobile app, you should 
have an understanding of:

* Using Eclipse IDE for development
* Basic understanding of the Android Java framework
* How to use GitHub for source code management

If you are completely new to any of the above, here are a few links to help get 
you started:

* Eclipse - installation and set up - http://eclipse.org/
* Android development environment - https://developer.android.com/
* Android app development - getting started - http://www.vogella.com/android.html
* Git - http://git-scm.com/
* GitHub getting started (and Egit for linking up to Eclipse) - http://www.eclipse.org/egit/ 


Getting Started
---------------
* Set up your development environment (Eclipse and Android framework)
* Create a fork of the `oppia-mobile-android` repository in GitHub
* Clone your new GitHub repository to your machine
* Create a project in Eclipse connected to this repository
* Ensure that you are able to compile and run (either on your physical Android 
  phone or on an Android Virtual Device) 
  
Please ensure that you are able to compile and run the core version of the app
before you start to make any changes to the code.

Server Connection 
-----------------
Assuming you have set up and installed you own OppiaMobile server, clearly 
you'll want your users to connect to this by default.

The core OppiaMobile android app is configured to point to our demonstration 
server (http://demo.oppia-mobile.org). To have your version of the app 
automatically point to your server:

* Open the ``/res/values/strings.xml`` file
* Change the ``prefServerDefault`` string to be the url to your server

Design/Layout
-------------
For changes to the design/layout such as changing the logo in the header, colour
scheme etc., this should be fairly straightforward and you should look at the 
following files in which to make these changes:




For more significant changes to the interface over and above changing the basic 
colour scheme and header etc, then this will require more substantial updates 
and familiarity with the code base.
 

Splash Screen
-------------


Preloading Courses
-------------------
If you would like to distribute your app with some courses preinstalled, for 
example if you have a lot of phones you would like set up with the same set of 
courses, then follow these steps:

* Place the course zip file(s) in the ``assets/www/preload/courses/`` directory
* Add the following lines to the ``doInBackground`` method of 
  ``org.digitalcampus.oppia.task.UpgradeManagerTask``::

		if(!prefs.getBoolean("upgradeVXXX",false)){
			Editor editor = prefs.edit();
			editor.putBoolean("upgradeVXXX", true);
			editor.commit();
			publishProgress("Upgraded to vXXX");
			payload.setResult(true);
		}

  where ``XXX`` is the new version number. The first time the app is installed 
  and run, the courses will be automatically installed.
  
* To subsequently distribute an updated version of the app (with new versions of
  the courses), then you will need to add another code block (with new version 
  number) to trigger the automatic installation of the updated/new courses.

Preloading Media Files
----------------------

Registration Form
------------------

Other Activity Types
--------------------

.. _clientappdist:

Application distribution and auto-updating
------------------------------------------



