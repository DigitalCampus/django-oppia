OppiaMobile Server Permissions
================================

There are various permissions associated with users in OppiaMobile, some based 
on the default Django users system and others based on extra permissions the user
has been specifically given.

* Admin User - this is the standard Django superuser 
  (https://docs.djangoproject.com/en/1.8/topics/auth/default/) - a typical user 
  with this role would be a system/server administrator
* Staff - this is the standard Django staff user 
  (https://docs.djangoproject.com/en/1.8/topics/auth/default/) - a typical user 
  would be a project manager/officer, college or ministry staff, essentially 
  users who need to access all the data/reports within the server, but not 
  necessarily responsible for the technical maintenance or server level admin.
* Teachers/Students - in Django permissions terms, both teachers and students 
  are standard users. The only difference between them is that a teacher has 
  been assigned the teacher status to a particular cohort of students. A cohort 
  is just a group of teachers and students assigned to a particular set of 
  courses. A user may have the role of teacher on one set of courses, but then 
  be a student on other courses.



Permissions on the OppiaMobile Server dashboard:
------------------------------------------------

+------------------------+---------------+---------------+---------------+---------------+
| Activity/Action        | Admin User    | Staff         | Teacher       | Student       |
+========================+===============+===============+===============+===============+
| Login                  | Yes           | Yes           | Yes           | Yes           |
+------------------------+---------------+---------------+---------------+---------------+
| Access Django Admin    | Yes           | No (1)        | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| Upload Course          | Yes           | Yes           | No (2)        | No (2)        |
+------------------------+---------------+---------------+---------------+---------------+
| Bulk Upload Users      | Yes           | No            | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| View Cohorts           | Yes           | Yes           | Yes (3)       | No (4)        |
+------------------------+---------------+---------------+---------------+---------------+
| Add New Cohort         | Yes           | Yes           | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| Edit Existing Cohort   | Yes           | Yes           | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| View course list       | Yes           | Yes           | Yes (5)       | Yes (5)       |
+------------------------+---------------+---------------+---------------+---------------+
| View draft courses     | Yes           | Yes           | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| View course recent     | Yes           | Yes           | Yes (6)       | No (7)        |
| activity               |               |               |               |               |
+------------------------+---------------+---------------+---------------+---------------+
| View course activity   | Yes           | Yes           | Yes (6)       | No (7)        |
| detail                 |               |               |               |               |
+------------------------+---------------+---------------+---------------+---------------+
| View course quizzes    | Yes           | Yes           | Yes (6)       | No (7)        |
+------------------------+---------------+---------------+---------------+---------------+
| View student activity  | Yes           | Yes           | No (6)        | No (7)        |
| (all activity)         |               |               |               |               |
+------------------------+---------------+---------------+---------------+---------------+
| View student activity  | Yes           | Yes           | Yes (6)       | No (7)        |
| (for specific course)  |               |               |               |               |
+------------------------+---------------+---------------+---------------+---------------+
| View student activity  | Yes           | Yes           | Yes (6)       | No (7)        |
| (for specific cohort)  |               |               |               |               |
+------------------------+---------------+---------------+---------------+---------------+
| View server level      | Yes           | Yes           | No            | No            |
| analytics              |               |               |               |               |
+------------------------+---------------+---------------+---------------+---------------+
| Upload media files     | Yes           | Yes           | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| Upload activity logs   | Yes           | Yes           | No            | No            |
+------------------------+---------------+---------------+---------------+---------------+
| Change password and    | Yes           | Yes           | Yes (own      | Yes (own      |
| update user info       | (any user)    | (any user)    | only)         | only)         |
+------------------------+---------------+---------------+---------------+---------------+
| Delete user account    | Yes (from     | No            | Yes (own      | Yes (own      |
|                        | admin pages)  |               | only)         | only)         |
+------------------------+---------------+---------------+---------------+---------------+
| Export user data       | Yes           | Yes           | Yes (own      | Yes (own      |
|                        | (own only)    | (own only)    | only)         | only)         |
+------------------------+---------------+---------------+---------------+---------------+


Notes:

1. Staff are able to access the Django admin URL, however they do not have 
   permissions to view any of the data models or actual data through this
2. Any user (teacher or student) may be given permissions to upload courses by 
   changing the 'can upload' field in their UserProfile to be true.
3. Teachers may only view cohorts that they are teachers in.
4. Students may view their own activity within a cohort
5. Students and Teachers may view all the courses available on the server, 
   except those that are still in draft stage
6. A teacher may only view the activity for courses they are assigned to be 
   teachers on, and then only for the students in the cohorts they are teachers 
   in.
7. Students may see their own activity within a course or cohort - but not 
   anyone elses



