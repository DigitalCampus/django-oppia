Settings and Defaults
========================

The OppiaMobile Android app makes use of the Android build system to define at compile time some of the settings for the project, so you don't need to modify any source code. This is done by reading a file in the root of the project called ``oppia-default.properties`` and creating all the necessary BuildConfig values.

If you want to overwrite any of this settings, create a new file named ``custom.properties`` and define any value of the list below that you want to override. Note that you don't need to define all the values again, simply the ones you want to override, and the rest will use the default value.

**IMPORTANT**: The ``custom.properties`` file is ignored by Git in order to hide private configuration settings (like API keys), so any changes you make to it will not be visible in your repository. 

List of configurable values
---------------------------

General
^^^^^^^

* ``MINT_API_KEY`` (string): the Splunk Mint API key to use for the crash reports
* ``OPPIA_SERVER_DEFAULT`` (string): the initial Oppia server URL. By default, the demo server https://demo.oppia-mobile.org/
* ``SESSION_EXPIRATION_ENABLED`` (boolean): enable that the session of the current user expires after a certain inactivity time. False by default
* ``SESSION_EXPIRATION_TIMEOUT`` (int): seconds of inactivity to expire a user's session (only works if the previous one is set to true)
* ``DEVICEADMIN_ENABLED`` (boolean): enable de remote admin functionality. False by default

Local admin settings (all false by default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``ADMIN_PROTECT_SETTINGS`` (boolean): enable the admin password protection functionality
* ``ADMIN_PROTECT_COURSE_DELETE`` (boolean): protect course deletion by admin password
* ``ADMIN_PROTECT_COURSE_RESET`` (boolean): protect course reset by admin password
* ``ADMIN_PROTECT_COURSE_INSTALL`` (boolean): protect course installs by admin password
* ``ADMIN_PROTECT_COURSE_UPDATE`` (boolean): protect course update by admin password

Main menu configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``MENU_ALLOW_MONITOR`` (boolean): show the "Monitor option" in the main menu
* ``MENU_ALLOW_SETTINGS`` (boolean): show the "Settings" option in the main menu
* ``MENU_ALLOW_COURSE_DOWNLOAD`` (boolean): show the "Install courses" option in the main menu
* ``MENU_ALLOW_LOGOUT`` (boolean): show the "Logout" option in the main menu
* ``DOWNLOAD_COURSES_DISPLAY`` (int): max number of courses installed in wich the "download more courses" button still appears in the main activity. By default, just one.
