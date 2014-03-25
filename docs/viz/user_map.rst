.. _usermap:

Setting up the User Map Visualization
=====================================

To set up the user map visualization to reflect the your users' location on your
server:

#. Create accounts on:
	  * `ipaddresslabs <http://ipaddresslabs.com/>`_
	  * `geonames <http://www.geonames.org/>`_
	  * `cartodb <http://cartodb.com/>`_
	  
#. Set up a table your CartoDB account with the following field names/types:
	* lat (number)
	* lng (number)
	* total_hits (number)

#. Edit the ``oppia/utils/cartodb_update.py`` to update the ``cartodb_table`` 
   variable with the name of your table in CartoDB.
   
#. Run the following :ref:`utility <utilities>` scripts:
	* ``ip2location.py <IP Address Labs API Key> <Geonames username>``
	* ``cartodb_update.py <CartoDB Account Name> <CartoDB API Key>``

#. (optional) If you would like the map to be automatically updated, you can set 
   up a shell script and crontab task to automatically run the 2 scripts from 
   step 4.

#. Edit ``oppia/templates/oppia/viz/map.html`` to embed your map from CartoDB
