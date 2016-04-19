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

.. _utilities_media_scan:
	
media_scan.py
-------------

This will scan a given directory of video files and create a collection of image
screenshots from throughout the video, along with a file containing all the code
(md5 digest, video length, filesize etc) that you can cut and paste into your 
Moodle page.

You will need to have ``ffprobe`` installed to be able to run this script. This 
can be downloaded from: `<http://ffmpeg.org/ffprobe.html/>`_

Usage: ``python media-scan.py /home/input/video/dir/ /home/output/dir/``

The first parameter is the input directory (where all your videos are stored).

The second parameter is the directory to output all the images and video tags 
code.

The following optional parameters are also available:

* -f 
  This determines the number of images that will be created for each video 
  (they will be evenly divided between the length of the video). Example usage:

  ``python media-scan.py /home/input/video/dir/ /home/output/dir/ -f 10``

  This will create 10 video screenshot images for each video in the input 
  directory.
  
  The default is 5 images per video
  
* -w
  This determines the width in pixels of the output images. Example usage:
  
  ``python media-scan.py /home/input/video/dir/ /home/output/dir/ -w 500``
  
  With this all the images will be 500 pixels wide
  
  The default is 250.

media_url_check.py
-------------------
This script checks the urls of all the media activities in uploaded courses. 
This helps to prevent your users getting file not found errors when downloading
the videos included in your courses.

Usage: ``python media_url_check.py``

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

tidy_upload_dir.py
-------------------
This script checks the upload course directory (as defined in the Django 
settings.py file) for any course packages that are now obsolete. 

Usage: ``tidy_upload_dir.py``

.. note::
	For this script to run successfully, you will need to have the your 
	virtualenv activiated (if applicable) and environment variables set to point
	to your Django settings file - similar to how you set up the 
	:ref:`OppiaMobile cron task <installcron>`