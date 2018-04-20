Configuring your own version of the app
===========================================

Once you've cloned the OppiaMobile Android app code and check you can compile and run the app on your device, there are 
some changes you should make to the configuration.

The main reason to make these changes is so that you can:

* Submit your app to the Google Play Store - you won't be able to submit an unchanged clone of the core version to 
  Google Play as the package name is already used.
* Receive automatic notifications of any errors your users may get when using the app
* Automatically have the app connect to your OppiaMobile server 


Rename applicationId
---------------------------

In prior versions of OppiaMobile, it was needed to refactor all the references to the ``R.java`` class, but now it can be done dinamycally at build time thanks to the benefits of Gradle.
Update the ``app/build.gradle`` changing the ``applicationId`` value to a new one, keeping with the 'reverse url' type notation, so
for example, replace ``org.digitalcampus.mobile.learning`` with ``org.myorgname.myproject.oppia``.


Google Cloud Messaging
---------------------------

The app uses the Google Cloud Messaging platform to receive push messages. You need to configure your own API key from the Google developers console as explained in the :ref:`registering-gcm` section of the documentation.

This is mandatory, as the ``google-services`` plugin checks that your package name and ``applicationId`` match with the one that appears in the configuration JSON file.

If you are not going to use this functionalities, you can just edit the current ``google-services.json`` file in your project ``app`` folder, replacing the value of the ``"package_name"`` property with your own package name. The current configuration file is a dummy one, so no need to worry about it affecting your code.


Automatic error reporting 
--------------------------------------

Update the `MINT_API_KEY` setting to the specific key you have generated for your app.


Default server connection 
-------------------------------------

Assuming you have set up and installed you own OppiaMobile server, clearly you'll want your users to connect to this by 
default.

The core OppiaMobile android app is configured to point to our demonstration server (http://demo.oppia-mobile.org). To 
have your version of the app automatically point to your server, you need to update the ``OPPIA_SERVER_DEFAULT`` value in
the settings file (see  :ref:`_settings_values` for more info on this topic).

* Open the ``/res/values/untranslated.xml`` file
* Change the ``prefServerDefault`` string to be the url to your server

App title and welcome message
------------------------------------

To update your app title, you just need to update the strings in ``app/res/values/strings.xml`` and 
``app/res/values/untranslated.xml``

For the app title, you'll need to update:

* ``app_name`` string in ``app/res/values/untranslated.xml``
* ``title_welcome`` string in ``app/res/values/strings.xml``

For updating the welcome message, you'll need to update:

* strings ``fragment_welcome_title``, ``fragment_welcome_desc`` and ``fragment_welcome_login_info`` in 
  ``app/res/values/strings.xml``

App logo
---------------

To use a different logo for your app, place your app logo in the drawable folder and update the following:

* In ``AndroidManifest.xml`` update ``android:icon="@drawable/dc_logo"`` to point to your logo (eg @drawable/my_logo)
* In ``org.digitalcampus.mobile.learning.application.MobileLearning`` class update ``public static final int APP_LOGO = R.drawable.dc_logo;`` to point to you logo (eg R.drawable.my_logo)

