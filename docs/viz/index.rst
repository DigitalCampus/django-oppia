.. _visualizations:

Visualizations
===============

.. toctree::
   :maxdepth: 1
   
   user_map

Creating visualisations of the data in OppiaMobile is a work-in-progress, 
currently there are 2 main visualisations available:

Summary Overview
----------------
This gives a one-page overview of the activity on your OppiaMobile server and 
can only be access by users with the is_staff status. The summary overview page 
gives graphical representations of:

* User Registrations
* Activity by Country
* Course Downloads
* Course Activity

.. note::
	All the statistics in the summary overview and map will exclude any 
	activity made by users who have the is_staff status.

User Map
--------
This shows a map of the locations of the users and activity on your OppiaMobile 
server. 

.. note::
	By default this map shows the users from the http://demo.oppia-mobile.org 
	server. To see a map of the users on your server, you will need to configure
	this, see the :ref:`user map setup instructions<usermap>`. 