OpenWASH Content Adaptation Process
=========================================


   "OpenWASH is a set of innovative learning resources launched in 2016 by The Open University in partnership with World 
   Vision Ethiopia and UNICEF through the ONEWASH PLUS programme, funded by UK aid from the UK Government. OpenWASH 
   supports the Government of Ethiopia’s One WASH National Programme which aims to radically improve the provision of 
   safe water and sanitation and bring significant benefits to millions of people."
   `OpenWASH website <http://www.open.edu/openlearnworks/OpenWASH>`_
   
Digital Campus, supported by `mPowering Frontline Health Workers <http://mpoweringhealth.org>`_, has adapted these 
Creative Commons licensed learning resources to be mobile optimised and run on the OppiaMobile learning platform. This 
document describes the adaptation process.

1. Importing into a local Moodle
---------------------------------

From the OpenLearn site, the resources may be downloaded in a variety of formats, however for this adaptation process we 
required the courses in standard Moodle format, so that we could easily collaborate and edit/format the course.

Unfortunately, OpenLearn no longer provides the option to download courses in Moodle backup format, although it used to. 
The format most suitable to us to import was the OUXML format - this is an internal OU format used for all their 
courses, so can be then exported for print or web.

A script was developed to create a Moodle backup formatted file of all the XML content, plus images, which could then be 
restored into a Moodle server.

The script and associated documentation can be found on GitHub: https://github.com/DigitalCampus/OUXMLConverter 

2. Review of imported content
-------------------------------

Once the content had been imported into Moodle, a first export to OppiaMobile was done and the initial quality check 
performed. The key areas that we were looking for were:

* consistency in style sheet usage
* formating of info, definition, in-line question and case study boxes
* image importing

As a result of this first check the following updates were made:

* activity icons added, where activities/pages did not have a suitable icon
* formatting of the end-of-session self-assessment questions 
* fixes to style sheet formatting where necessary

3. Additional quiz questions
------------------------------

In the original course content, self-assessment questions (SAQs) are provided at the end of each study session. Many of 
these questions are unsuitable for automatic marking within the OppiaMobile app - as, for example, they require the 
student to write longer text or complete a table of information. These questions have been retained in the mobile 
adapted version, but only as HTML pages, rather than as a quiz activity.

Additional self-assessment quiz questions (in Moodle quiz format) have been developed and added to each study session. 
These questions are of a more basic type than the original SAQs (eg short answer, multichoice) - however they allow the 
student to have their responses marked automatically in the OppiaMobile app.


4. Quality assurance check
----------------------------

.. note::
	Since these courses had already been very well developed by subject experts and copy edited, our QA check did not 
	include copy editing or validating the correctness of the content/information in these courses.
	
The courses were exported to OppiaMobile and the content reviewed again within the OppiaMobile app. 

We also ran the quiz questions through our quiz checker script - which tests submitting each possible response through 
our quiz engine to ensure that the marking and scoring is correct as well as helping with spelling and grammar checking.

5. Creating non-country specific version
-----------------------------------------

The final part of the adaptation was to create a non-country specific version. The original courses have a lot of 
Ethiopia specific references, so the idea of removing these is to make it easier to them adapt and re-use the course in 
other countries.

Copies of each course were made and a database scan performed to identify the pages which include Ethiopia specific 
references. These pages were then updated to provide more general references, the references updated include:

* Ethiopia
* woreda
* kebele						
* health extension worker
* HEW
* health development army
* HDA
* health promotion worker
* Addis
* Oromo
* Oromia
* tigray
* amhara
* health post
* MoH
* FMoH
* Adama
* korales
* Ministry of Water and Energy
* Mekelle University
* Bahir Dar
* Regional Health Bureau
* Ministry of Works and Urban Development
* MoWE
* MoWUD
* MFSH
* CLTSH
* Town Water Board
* Hawassa
* Wechale
* birr
* gondar
* Operation and Maintenance Department
* Wuha Agar
* National Fluorosis Mitigation Project
* debo

The script used to scan the content for these terms can be found here: 
https://github.com/DigitalCampus/ou-content-adaptation-scripts/blob/master/helper/OpenWASH-global-editing-links.php


6. Final QA
---------------

A final export to OppiaMobile of both the Ethiopia specific and non-country specific versions, then reviewed again on a 
mobile device.


