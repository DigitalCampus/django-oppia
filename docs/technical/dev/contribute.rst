Contributing to OppiaMobile
=============================

To get started and help contribute to OppiaMobile, the first steps will be:

#. Clone the server and get a local version running on your machine
#. Clone the app and have it compiling and deploying to your mobile device
#. Set up Moodle installation and the OppiaMobile Moodle export block
#. Create a course in Moodle and deploy this to your server and then on to your device (using your new locally installed 
   platform components)
#. Change your app name and theme and have this compiling and installing


Note that we've deliberately left out the specifics of these steps here - since they should already be elsewhere in these 
docs (if not, then see below...)

Once you have the basic platform running locally, there are a lot of different ways you can start contributing, even 
before getting fully submerged in the whole code base:

* Provide feedback and recommendations on the documentation (both the processes/descriptions and the overall 
  navigation of how these doc pages are structured)
* Provide feedback and input on the overall user interface and process to publish a course, navigate the server 
  dashboard and use the app
  
Submitting code contributions
---------------------------------------

If you have made updates (new functionality, bug fixes etc) that you'd like to 
contribute back to the core version of OppiaMobile, then please issue a "pull 
request".

You can find info here on how to issue a pull request: https://help.github.com/articles/using-pull-requests/

Creating small, specific pull requests (matched to an issue in GitHub issue 
tracker), will make it much easier and quicker (and also more likely) that your 
changes can be incorporated into the core version.

We're keen to acknowledge those who have contributed to the development of 
OppiaMobile, so please also send us your attribution information (name, 
organisation etc), so we can include you in the about/acknowledgements section 
of the app.

  
Other ways to contribute
-------------------------

Whilst the GitHub issue lists provide the core of the issues, bug fixes and enhancements - these can be a little 
impenetrable to anyone who is unfamiliar with the detail of how the platform components work, so here are some 
suggestions for how you could contribute (in no particular order, and some may depend on your experience and interest):

* how we could set up continuous integration for both app and server code (esp when code is checked in to Github)
* how we could integrate with a crowd-sourced translation service (or if you're already able to provide translations)
* code improvements & refactoring, eg items under https://github.com/DigitalCampus/oppia-mobile-android/labels/refactoring%2Freview and report output from SonarCloud: https://sonarcloud.io/dashboard?id=oppia-mobile-android%3Aapp 
* improve testing coverage
* keeping code up to date with latest Django and Android frameworks - eg, refactoring for any deprecated functions
* ideas to improve gamification beyond points & badges, although...
* ... we would like to integrate with Mozilla Open Badges
* improve media embedding in Moodle and subsequent publishing to Oppia
* integration with xAPI (https://xapi.com/ - 'programmable elearning and experience tracking')
* allowing login with users existing Google, Facebook, Twitter accounts

Another area that we are very much interested in, but needs some research and planning is around personalised/adaptive 
learning - so being able to tailor course content based on users existing knowledge & experience or responses to pre-tests.

All of the above are improvements and enhancements that we've wanted to do for a long time, but any contributions (on 
the list above or not) will help us keep OppiaMobile running and improving for its users.

