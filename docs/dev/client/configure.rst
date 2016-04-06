Configuring your own version of the app
===========================================

Once you've cloned the OppiaMobile Android app code and check you can compile and run the app on your device, there are 
some changes you should make to the configuration.

The main reason to make these changes is so that you can:

* Submit your app to the Google Play Store - you won't be able to submit an unchanged clone of the core version to 
  Google Play as the package name is already used.
* Receive automatic notifications of any errors your users may get when using the app
* Automatically have the app connect to your OppiaMobile server 


Rename package
---------------------------

Update the package attribute on manifest tag in AndroidManifest.xml (keeping with the 'reverse url' type notation), so 
for example, replace ``org.digitalcampus.mobile.learning`` with ``org.myorgname.myproject.oppia``

Classes to update 
----------------------------

Replace all instances of ``import org.digitalcampus.mobile.learning.R;`` with ``import org.myorgname.myproject.oppia.R;``.
This import is used in almost all the classes, so it will be easier to use a search and replace on the whole 
src/main/java directory.


Automatic error reporting 
--------------------------------------

Update the `MINT_API_KEY` in application/MobileLearning.java to the specific key you have generated for your app.


Default server connection 
-------------------------------------

Assuming you have set up and installed you own OppiaMobile server, clearly you'll want your users to connect to this by 
default.

The core OppiaMobile android app is configured to point to our demonstration server (http://demo.oppia-mobile.org). To 
have your version of the app automatically point to your server:

* Open the ``/res/values/untranslated.xml`` file
* Change the ``prefServerDefault`` string to be the url to your server
