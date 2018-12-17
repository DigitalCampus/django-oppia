Branches and Release Process
================================

This page describes the code branch management convention OppiaMobile developers (for all 3 components), and the release 
process/checklist.

Branch Management
---------------------------------

#. A new dev release branch is created (e.g. 'v1.2.3') - this is the branch to which all fixes and issues will be merged 
   into for testing, before being merged into the master branch.
#. A new branch is created for each issue to be fixed in the development cycle (e.g. 'issue-567') 
#. Code is developed on the issue branch

A couple of exceptions to the above process:

#. very minor fixes (that don't warrant their own issue branch) may be applied directly to the release branch
#. database updates/re-structuring will be applied directly on the release branch. This saves conflicts if their are 
   database updates on multiple issue branches
   
Server Release Process/Checklist
----------------------------------

Before making pull request from issue branch to release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Add/update unit/automated tests
#. Run Django tests framework and confirm all tests are passing [add link/info]
#. Run Sonar test framework [add link/info]
#. Check code for PEP8 compliance [add link/info]
#. Add/Update documentation for any new or changed functionality/processes/settings

Merging issue branch into release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Merge code in (as above and resolve and conflicts from other branches)
#. Run django tests framework and confirm all tests are passing
#. Run Sonar tests framework
#. Update release notes (adding issue resolved)
#. Close issue on Github


Merging release branch into master, for final release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. merge code in (as above and resolve and conflicts from other branches)
#. Run django tests framework
#. Run Sonar tests framework
#. date the release (on release notes)
#. tag
#. update roadmap
#. release...

Creating new release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


App Release Process/Checklist
-----------------------------

Before making pull request from issue branch to release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merging issue branch into release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merging release branch into master, for final release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating new release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Block Release Process/Checklist
---------------------------------

Before making pull request from issue branch to release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merging issue branch into release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merging release branch into master, for final release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating new release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^