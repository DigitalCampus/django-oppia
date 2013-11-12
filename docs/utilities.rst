Utilities
=========

Any utility scripts can be found in the ``django-oppia/oppia/utils`` directory.


media-scan.py
-------------

This will scan a given directory of video files and create a collection of image
screenshots from throughout the video, along with a file containing all the code
(md5 digest, video length, filesize etc) that you can cut and paste into your 
Moodle page.

You will need to have ``ffprobe`` installed to be able to run this script. This 
can be downloaded from: `<http://ffmpeg.org/ffprobe.html/>`_

The basic usage is as follows:

``python media-scan.py /home/input/video/dir/ /home/output/dir/``

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


