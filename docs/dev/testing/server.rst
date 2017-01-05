Release Process for OppiaMobile Server
=======================================

#. Create automated unit tests before development of new feature begins
#. Develop code
#. Test locally on issue branch (ensuring up to date with the current release branch)
#. Update/add documentation as necessary
#. Merge into release branch and re-test (both manual and automated tests)
#. Copy onto staging server and re-test
#. Merge release branch into master branch, update version numbers and tag with new version no
#. Deploy to live server


Specific tests that need to be applied for each release:

* creation and testing of new/updated course content

