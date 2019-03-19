Issue, Branch and Release Processes
====================================

This page describes the issue and code branch management convention that 
OppiaMobile follows (for all 3 components), and the release process/checklist.

Issues, Branches and Pull Requests
------------------------------------

Issue branches should be related to only one issue, and be based on the current
release branch. This avoids situations where issue branches cannot be merged 
into the release branch as they are dependent on other issue branches.

There may be some cases where multiple issues are addressed on the same issue 
branch, but then these should be very closely related issues.

Similarly, pull requests should be related to one issue (and issue branch).

Pull requests should include new/updated documentation and automated tests. The 
documentation and tests are part and parcel of the technical development work 
for any issue.


Branch Management
---------------------------------

#. A new dev release branch is created (e.g. '1.2.3') - this is the branch to 
   which all fixes and issues will be merged into for testing, before being 
   merged into the master branch.
#. A new branch is created for each issue to be fixed in the development cycle 
   (e.g. 'issue-567') 
#. Code is developed on the issue branch

A couple of exceptions to the above process:

#. very minor fixes (that don't warrant their own issue branch) may be applied 
   directly to the release branch
#. database updates/re-structuring will be applied directly on the release 
   branch. This saves conflicts if there are database updates on multiple issue
   branches
   
Server Release Process/Checklist
----------------------------------

Before making pull request from issue branch to release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Add/update unit/automated tests
#. Run Django tests framework and confirm all tests are passing 
   [:doc:`../testing/index`]
#. Run Sonar test framework [add link/info]
#. Check code for PEP8 compliance [add link/info]
#. Add/Update documentation for any new or changed functionality/processes/
   settings
#. Update the relevant GitHub project to show the issue is for review 

Merging issue branch into release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Merge code in (as above and resolve and conflicts from other branches)
#. Run Django tests framework and confirm all tests are passing
#. Run Sonar tests framework
#. Update release notes (adding issue resolved)
#. Close issue on Github


Merging release branch into master, for final release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Merge code in (as above and resolve and conflicts from other branches)
#. Run Django tests framework
#. Run Sonar tests framework
#. Date the release (on release notes)
#. Tag the release in git
#. Update roadmap
#. Release...

Creating new release branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. 

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