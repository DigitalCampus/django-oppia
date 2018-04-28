.. _utilities:

Utilities
=========

All utility scripts can be found in the ``django-oppia/oppia/utils`` directory.

cartodb_update.py
-----------------
This script updates the user location map in `CartoDB <http://cartodb.com/>`_

Usage: ``cartodb_update.py <CartoDB Account Name> <CartoDB API Key>``

:ref:`More information <usermap>` about how to set up and configure the location
map

.. note::
	For this script to run successfully, you will need to have the your 
	virtualenv activiated (if applicable) and environment variables set to point
	to your Django settings file - similar to how you set up the 
	:ref:`OppiaMobile cron task <installcron>`
	
	
ip2location.py
-----------------
This script converts the IP addresses from the Tracker log to a latitude/
longitude location, for displaying on the CartoDB user map visualization.

Usage: ``ip2location.py <IP Address Labs API Key> <Geonames username>``

:ref:`More information <usermap>` about how to set up and configure the location
map

.. note::
	For this script to run successfully, you will need to have the your 
	virtualenv activiated (if applicable) and environment variables set to point
	to your Django settings file - similar to how you set up the 
	:ref:`OppiaMobile cron task <installcron>`


oppia-schema.xsd
-------------------
This is the XML Schema Definition for the course XML file, it is used by the 
OppiaMobile server to check that any courses uploaded are valid OppiaMobile 
course packages.

