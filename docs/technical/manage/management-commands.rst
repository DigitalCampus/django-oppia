OppiaMobile Server Management Commands
=========================================
Django's manage.py runs a variety of Django admin tasks, and each project can add their own. OppiaMobile bundles some management commands
to perform some tasks that make more sense to be executed from the command line than include them in the admin user
interface of the web page.

To run any of this commands, just use the ``manage.py`` script like with the common Django admin actions (i.e. activating
the virtualenv and setting your path to the server folder.

To view all the commands available in any Django project, you can type ``manage.py help`` to view a list of them, grouped
by Django app. Also, you can access the help for a command typing ``manage.py help <command_name>``.

Available commands
....................

cartodb_update
-----------------
This script updates the user location map in `CartoDB <http://cartodb.com/>`_

:ref:`More information <usermap>` about how to set up and configure the location
map	

cleanup_quizzes
---------------------
**Cleans up old data** (quizzes and questions) **that is not relevant anymore**.
It removes all the quizzes and its related data (properties, questions, correct answers, etc) that are not part of a
course anymore and don't have any attempt. Before actually deleting the data, the command prompts the user for confirmation.

cleanup_uploads
---------------------
**Cleans up any old files in the oppia uploads directory**.
Cleans the temporary zip files uploaded to the server that are no longer needed. It also checks that every course in
the server has its related course package so it can be downloaded, printing a warning for each of them that doesn't satisfy this.

generate_media_images
---------------------
**Generates sample media images**
Creates sample image files (snapshots/screenshots) from any media that has been uploaded

ip2location
-----------------
This script converts the IP addresses from the Tracker log to a latitude/
longitude location, for displaying on the CartoDB user map visualization.

:ref:`More information <usermap>` about how to set up and configure the location
map

media_url_check
---------------------
**Checks the media download urls to ensure they are valid links**
It checks all the links for media files that are embedded in course to ensure they are valid links, printing a warning for any media file
that is referenced in a course, but the media file is not actually available for download.

remove_duplicate_quiz_attempts
---------------------------------
**Removes any duplicate quiz attempts based on instance_id**

remove_duplicate_trackers
---------------------------
**Removes any duplicate trackers based on UUID**

update_short_answer_scores
---------------------------
**Updates the scores for short answer questions**.
It receives an additional parameter pointing to a CSV file that includes the response attempts to update and its new
scores. It then goes to the related quiz attempts and updates their total scores and checks the pass threshold with the new score.

update_summaries
---------------------
**Updates course and points summary tables**.
A shortcut to execute the cron task to update course activity and points summary tables.



	


