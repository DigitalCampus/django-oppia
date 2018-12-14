Moodle Block Installation
==========================

There are 2 main methods for installing the OppiaMobile Export Moodle Block, 
depending on how you are able to access your Moodle server. After you have 
installed the block, please see the instructions below for setting up the 
connection to the OppiaMobile server (further below).

Full server admin rights on your Moodle (e.g. if you 'own' the server)
-----------------------------------------------------------------------

* This would be the preferred approach
* Clone the GitHub repository https://github.com/DigitalCampus/moodle-block_oppia_mobile_export 
  into your `moodle/blocks/` directory
* You'll need to rename the generated directory `moodle-block_oppia_mobile_export` to be just `oppia_mobile_export`
* Visit the admin notifications page on your Moodle server to trigger installing the block 


Local rights for your Moodle installation (e.g. on shared hosting)
------------------------------------------------------------------
* Download the zip file of the latest release of the block at: https://github.com/DigitalCampus/moodle-block_oppia_mobile_export/releases
* Open the zip file and rename the root directory to be `oppia_mobile_export` (instead of `moodle-block_oppia_mobile_export`) - you may need to unzip and re-zip this file depending on your operating system.
* In your Moodle server  under the site admin -> plugins, select 'install plugins'
* Upload your new zip file as a new block

Adding the block to your course
---------------------------------

Even once you have installed the block, you may not see it appearing in the your Moodle server. This is because we 
haven't yet added it for display. You can either add the block for individual courses or have it appear on all the 
courses on your Moodle server:

* Adding to a single course: on the course homepage, turn editing on, then in the 'Add a block' block, select the Oppia 
  Export Block to add to your course.
* Adding to all courses, see the `Moodle Block Settings documentation <https://docs.moodle.org/en/Block_settings>`_

Block configuration to connect to an OppiaMobile server
---------------------------------------------------------
Once the block is installed you will need to provide some settings to connect your Moodle server to an OppiaMobile server.
These settings are used to export the quiz and feedback activity questions, and also for directly publishing your course to OppiaMobile.
A Moodle server can be set up to connect to a number of different OppiaMobile servers (conversely and OppiaMobile server can support courses from different Moodle servers).
The basic set up is to provide a default OppiaMobile server for your Moodle server to connect to, so:

* in the oppia_mobile_export block settings, enter the url, username and api_key for your OppiaMobile server.
* for the url you only need to enter the base url (e.g. `http://demo.oppia-mobile.org/` rather than `http://demo.oppia-mobile.org/api/v1/`)
* for the username, use the username you use to log into the OppiaMobile server
* for the API key, you can obtain this when you log into the OppiaMobile server and visit your profile page

This will allow any teachers/admins on your Moodle server to publish to the specified OppiaMobile server. 

You may wish to add other connections (e.g. on a user by user basis, or to other OppiaMobile servers), you can do this from the block:

* select the 'add new server connection' option from the oppia_export_block
* enter the url, username and API key (as described in the info above)
* when you export your course using the block, you can select which connection you'd like to use.


