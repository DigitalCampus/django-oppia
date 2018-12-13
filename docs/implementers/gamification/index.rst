Points and Badges
====================

OppiaMobile awards points and badges to users based on their usage of the app and content.

.. note::
    All the points and badges are awarded by the server, so if the user is offline, they will 
    not see their points increase, instead these points will be awarded once their device is 
    next connected.

The points system is essentially a measure of engagement with the content - however it doesn't 
really give a picture of how much was understood. The badging provides confirmation that all 
the activities have been completed and that the user has met at least the pass threshold for 
each quiz included in the course.


Points
---------
Points are currently awarded as follows:

* 100 – creating an account
* 50 – downloading a course
* 20 – first time a quiz is attempted
* ? – depends on percentage score for a first attempt at a quiz. E.g. if the score is 75% on the 
  first attempt, 75 points will be awarded
* 50 – bonus for getting 100% on first attempt at a quiz
* 10 – each subsequent attempt at a quiz (max. once per day per quiz)
* 10 – completing an activity (max. once per day per activity)
* ? – video views – points are awarded for how long the video has been have watched, 5 points for 
  every 30 seconds watch, up to a maximum of 200 points. A bonus 20 points are given for the first 
  time in a day a particular video is watched

The points system is designed to encourage users to return to the courses regularly and engage in 
the activities.

The points awarded for each activity can be customised in the server settings. To change the criteria 
for the awarding of points, you'll need to look at the signals.py file in the server as this 
determines the criteria for points.


Badges and Completing Courses
------------------------------

Every activity has the concept of 'completedness' and to be awarded a badge the user must complete 
every activity in the course. The definitions of activities being completed of each activity type 
are given below:

* quiz - a quiz is completed if the user has obtained at least the pass threshold for the quiz.
* text/webpage - the page must be open for at least 3 seconds. Clearly this is not a very effective 
  measure of testing whether the user has fully read and understood the page content, however, 
  currently it is the only way of measuring that we currently have. We advise ensuring that the quiz 
  questions provide an effective measure of understanding the content.
* video - video/media files are embedded within text/web pages. The user must have the video running 
  for at least the length of the video. This may not correspond exactly to saying they have watched 
  the whole video - for example they may pause, fast-forward/rewind, and so have the video open for 
  the required time, but not actually have watched the video from start to finish.
* feedback - the user needs to answer all the questions
* file - the user simply needs to have opened the file

To change the criteria for assessing completedness of the activities, the getActivityCompleted() 
function for the relevant activity widget class in the app code will need to be updated.


.. note::
   The badge awarding is performed by the :ref:`Oppia cron task <installcron>`, so for badges to be 
   awarded, please ensure that the cron task is set up to run regularly.

Who can earn points/badges?
----------------------------

In the default settings:

* Admins and staff users do not earn points or badges for their activity in 
  courses.
* Teachers do not earn points or badges in the courses they are teachers on
* If non admin or staff users are given permissions to upload courses, then they
  will not earn points or badges in the courses they upload.

These defaults may be changed in the server settings.
