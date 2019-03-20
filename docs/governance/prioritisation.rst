Tech Dev Prioritisation Process
==============================================


Core OppiaMobile development takes place as a 2-week sprint per month, so the 
issues addressed need to be prioritised for the upcoming sprint.

Any developments, fixes, features etc must first be entered as issues in the 
relevant GitHub issue list. Issues entered should be tagged at least with a 
high/medium/low priority and whether it is a bug or enhancement. Any issues 
submitted will be reviewed for the tags to ensure the tags are correct and 
appropriate.

For a given sprint the open issues will be prioritised on the following basis 
(highest priority to lowest):

#. High priority bugs
#. Outstanding automated tests that need to be added for recent code updates
#. Code updates to ensure the code base passes the SonarQube analysis
#. Outstanding documentation for any recent code updates
#. Other open issues

Item 1 is clearly the most important, since high priority bugs will be those 
that directly affect the running and implementation of OppiaMobile.

Items 2, 3 and 4 should eventually be addressed as part and parcel of any 
feature/code updates - i.e. when code is updated (whether it is a new feature, 
or an improvement/bug fix on an existing feature), the automated tests and 
documentation should be included as part of the code update.

Item 5 is the area of prioritisation this document mainly focuses on.

Once items 1-4 have been scheduled and time estimated in the upcoming sprint, 
we will then know the remaining developer time available for item 5. 

Note that these sprints are for the core Digital Campus OppiaMobile developer 
team, other teams/developers may wish to work on specific features developments 
that are relevant to them.

For each sprint, the tasks will be added in the ‘queued for development’ column 
in the general development Github project. The core OppiaMobile developer team 
will make an initial suggestion on the tasks that will be included for item 5, 
based on discussions and information from the developer and community 
governance boards.

The suggested tasks for the sprint will then be shared with the developer 
governance board for their input, feedback and approval. In the interests of 
time, board members who do not provide input/feedback within the given 
timeframe, will be assumed to approve suggested task list.

Should the time estimate be incorrect (eg the scheduled tasks take 
shorter/longer time than expected)….

For a monthly sprint process:

* Week 1 - input/feedback/approval from the developer governance board
* Weeks 2 & 3 - code sprint takes place
* Week 4 - review and integration of the code developed, next suggested sprint 
  tasks are added, and the monthly cycle restarts.
  
  
