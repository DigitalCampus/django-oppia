Publishing your Moodle Course to Oppia
========================================

When you have completed :doc:`author`, or at least, are ready to test your 
course in the OppiaMobile app, then you will need to publish your course to the 
OppiaMobile server.

From the OppiaMobile Export Block in your Moodle course:

#. Select the ``connection`` you would like to use (see below: 
   :ref:`export_server_connections_explained`).
#. Select the ``stylesheet`` you would like to use.
#. Press the ``Export to Oppia Package`` button.
#. On the next page, you will see some options for quizzes and general course 
   settings (see below: :ref:`export_options_explained`)
#. After selecting/entering the options, press on ``continue`` button
#. You will then see the results of the export and an option to either download
   or publish the course (see below: :ref:`export_download_or_publish`)


.. _export_server_connections_explained:

Server Connections - Explained
-----------------------------------

There is not a 1-1 connection between a particular Moodle course and an 
OppiaMobile server. A Moodle course could be published to several OppiaMobile 
servers, and conversely, an OppiaMobile server could host courses from 
different Moodle servers.

So when you export a course from Moodle to OppiaMobile, you need to specify 
which OppiaMobile server you want to export to.

If you do not see the OppiaMobile server you'd like to export to, then you'll 
need to ``Add a new server connection``, providing:

#. Server name - this is just your reference 
#. The url to the OppiaMobile server
#. Username - your username for the OppiaMobile server
#. API Key - your API Key for the OppiaMobile server, you can obtain this by 
   logging into the OppiaMobile server and going to 'My Oppia' > 'Edit Profile'   

.. _export_options_explained:

OppiaMobile Export Options - Explained
----------------------------------------

Quizzes
~~~~~~~~

If your course has quizzes, then you will see a table of the quizzes with some 
options to select:

#. **No random questions** - if you don't want all the questions to show to the
   user then select the number of questions that should be shown. They will 
   appear in a random order, so don't use this if certain questions depend on 
   information from previous questions or info. 
#. **Show feedback** - when (if ever) should feedback about the users response #
   be shown.
#. **Allow try-again?** - should the user be shown the option to try the quiz 
   again straight after completing the quiz.
#. **Pass Threshold (%)** - what's the threshold (in percent) for the user to 
   pass this quiz.
#. **Availability** - when is the user allowed to access this quiz.
#. **Max number of attempts** - how many attempts can a user have at this quiz.


.. note::
   If the quiz is a pre-test, then only the **No random questions** option will
   be used, all other options will be ignored. The user will not receive any 
   feedback for pre-test questions, there is no pass threshold and the user can
   only attempt the quiz once.
   
Course Priority 
~~~~~~~~~~~~~~~~

To help specify the order in which courses should appear when users go to 
download courses in the given tag/category. And also when the course is 
displayed in the app main menu listing. For example, if you would like your 
courses to display in a particular order in which users should complete them.

Otherwise courses will display in alphabetical order in the app.

Course Tags
~~~~~~~~~~~~~

You must specify at least one tag for your course, these are used as the 
categories in the app. If no tags are given then users will not be able to find 
your course in the app course downloads.

Course default language
~~~~~~~~~~~~~~~~~~~~~~~~

The `ISO-639 code <https://en.wikipedia.org/wiki/ISO_639>`_ that should be used 
as the default language for the course content when displayed to users.

.. note::
   In general you do not need to change this from the default ``en`` if your 
   course has been set up correctly for multilingual content (see: :doc:`translations`)

Course Sequencing
~~~~~~~~~~~~~~~~~~

By default, this is set to ``none`` so a user will be able to jump around the 
course activities however they would like (with the exception of having 
completed the pre-test).

To prevent users 'jumping' around in this way, you can force users to complete 
the course content either by section/topic (select ``Sequencing within a 
section``) or though the whole course (select ``Sequencing through whole 
course``).

.. note::
   If your course includes quizzes, and you select ``Sequencing within a 
   section`` or ``Sequencing through whole course``, users must get at least 
   the quiz pass threshold to be able to progress to the next activity.

.. _export_download_or_publish:

Download or Publish? - Explained
----------------------------------------

In general, downloading the course is for when you would like to test the 
course on your own device first, before making available to users. So you can 
download the OppiaMobile .zip formatted package and install directly on your 
own device to check the course.

If you ``publish`` the course, then it will be live for any users of your app.

 