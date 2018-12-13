User and Permissions Management
===================================

Add a new user
----------------

Either:

#. Just register a new user (using the 'Register' link in the menu bar)

Or:

#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'Users' under the 'Authentication and Authorization' section
#. Select 'Add a new user' and complete the form

Bulk upload users
--------------------

#. From the menu bar, select 'Admin' > 'Upload users'
#. Prepare a CSV file with all the user info. You can create a CSV file in Excel. 
   Note that the column names are case sensitive and must be written exactly.
#. Upload the file
#. After processing you'll receive a report detailing the results

Remove a user
---------------

.. warning::
	Removing a user will delete all their activity logs and course progress. If you 
	would like to stop a user from accessing Oppia, but without deleting all their 
	activity logs, then use 'Block a user account' instead.
	
#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'Users' under the 'Authentication and Authorization' section
#. Browse or search for the user and select
#. In the bottom left, click on 'Delete'
#. You will be asked to confirm deletion of the user account
	
Block a user account
---------------------

#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'Users' under the 'Authentication and Authorization' section
#. Browse or search for the user and select
#. Untick the 'active' checkbox
#. Click on the save button (bottom right)

You can unblock a user account in a similar way - just tick the 'active' checkbox instead.

Reset user password
-----------------------

.. note::
    There is no way to find out what the original password was, as the passwords are stored in an encrypted format.
    
#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'Users' under the 'Authentication and Authorization' section
#. Browse or search for the user and select
#. Under the password field, follow the link and instructions to reset the password

Add/remove admin access permission
------------------------------------

.. warning::
	Admin accounts have permissions to add, edit and delete any or all of the data stored, 
	as well as create other Admin user accounts. Admin permissions should only be given to 
	users who really need it, and consider giving staff status instead.
	
#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'Users' under the 'Authentication and Authorization' section
#. Browse or search for the user and select
#. Tick/untick the 'superuser status' checkbox
#. Click on the save button (bottom right)

Add/remove staff access permission
-----------------------------------

#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'Users' under the 'Authentication and Authorization' section
#. Browse or search for the user and select
#. Tick/untick the 'staff status' checkbox
#. Click on the save button (bottom right)

Add/remove permission to upload courses
------------------------------------------

#. From the menu bar, select 'Admin' > 'Django Admin'
#. Select 'User Profiles' under the 'Oppia' section
#. Browse or search for the user and select
#. Tick/untick the 'Can upload' checkbox
#. Click on the save button (bottom right)