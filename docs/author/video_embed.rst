Using Video Content in OppiaMobile Courses
===========================================

When a user installs a course containing video content, the actual videos aren't
included in the course download content. The reason for this is that video files 
tend to be very large and users on slow connections are unlikely to be able to 
download large video files.

If a course contains video files that aren't available on the users phone, on 
the app homepage a message will appear that some video/media content is missing.

How to embed video files in OppiaMobile courses
-------------------------------------------------

#. Optimize your video for playback on mobile devices. User viewing videos on a 
   4 or 5 inch screen generally don't need super high quality as you may want to 
   use if projecting the video. At Digital Campus, we usually convert videos 
   into .m4v format using Handbrake (https://handbrake.fr/ - an open source tool 
   and works on most platforms)
#. Upload the converted video to the internet, so it's available for anyone to 
   directly download the full video file. If you have your own OppiaMobile 
   server, you could just set up a web available directory on there. Digital 
   Campus for example has a plain website 
   (http://downloads.digital-campus.org/media/) where we store the videos we're 
   using in our courses.
#. Generate the md5 checksum for your video. All operating systems will allow 
   you to generate an md5 checksum of a file. The md5 is essentially a unique 
   code to identify a file and it's contents. We use this for the videos, so 
   when a user download the video on their phone the app can verify they have 
   the complete video (and no broken/partial downloads) and the correct video.
#. Now you have md5 and the file uploaded to a server you can embed your video 
   into your page on Moodle using the following code:
   
   .. code-block:: json
   		
   		[[media object='{“filename”:”ghmp-basic-skills-20121001.m4v”,
   					”download_url”:”http://downloads.digital-campus.org/media/pnc/ghmp-basic-skills-20121001.m4v”,
   					”digest”:”3ec4d8ab03c3c6bd66b3805f0b11225b”}’]]IMAGE/TEXT HERE[[/media]]
   
   Just update the filename, download_url and digest (md5) to match your video 
   file details.
#. You can replace the ``IMAGE/TEXT HERE`` with either some text or a screenshot
   of you video. When your course is exported from Moodle, the export script 
   will use the supplied information to ensure the user downloads the correct 
   video.
#. You optionally supply a filesize (in bytes) and length (in seconds) as 
   follows:

   .. code-block:: json
	
	   [[media object='{“filename”:”ghmp-basic-skills-20121001.m4v”,
						”download_url”:”http://downloads.digital-campus.org/media/pnc/ghmp-basic-skills-20121001.m4v”,
						”digest”:”3ec4d8ab03c3c6bd66b3805f0b11225b”, 
						“filesize”:312345657, 
						“length”:360}’]]IMAGE/TEXT HERE[[/media]]
	
   Adding a filesize will inform the user how large the file is before they try
   to download and the length will be used to determine whether a user has 
   watched the whole video (or not).
#. [Optional - but probably convenient] You use the utility script 
   :ref:`/oppia/utils/media_scan.py <utilities_media_scan>` to generate the 
   embed code blocks for a whole directory of video files. This will also 
   automatically generate a set of screenshots from the video that you can use 
   for embedding.   
   

How can users get the video files
----------------------------------

There are two options for getting the video content onto users phones:

#. Download the video/media files directly onto the users SD card. This is most 
   likely the best option for projects which are providing phones to users as 
   the video files can be pre-loaded
#. Download via the app. When the app flags up that a video file is missing, 
   then the user can download directly to their phone. This is only likely to be
   feasible to users who are connected to wifi. So by default users will only be 
   able to download video files directly if they are connected to a wifi network. 
   This can be overridden in the app settings to allow downloading of video 
   files by allowing downloading using cellular network.

