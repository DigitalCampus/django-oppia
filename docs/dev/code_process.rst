Branches and Release Process
================================

The page describes how the core Oppia repositories are structured for developing and managing new features and fixes. The following process is applied to all 3 of the Oppia GitHub repositories (server, Android app and Moodle block).


#. A new dev release branch is created (e.g. 'v1.2.3') - this is the branch to which all fixes and issues will be merged into for testing, before being merged into the master branch.
#. A new branch is created for each issue to be fixed in the development cycle (e.g. 'issue-567') 
#. Code is developed on the issue branch
#. Once coding and testing of the feature is completed, the issue branch will be merged into the release branch
#. Once all the features for the release have all been merged into the release branch, integration testing then takes place, to ensure there are no conflicts.
#. The release branch is then merged into the master branch and the master branch is tagged with the release number

A couple of exceptions to the above process:

#. documentation (in the server repository) will be added directly into the master branch
#. very minor fixes (that don't warrant their own issue branch) may be applied directly to the release branch
#. database updates/re-structuring will be applied directly on the release branch. This saves conflicts if their are database updates on multiple issue branches