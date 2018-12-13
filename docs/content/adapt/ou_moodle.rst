Adapting Open University Moodle Content - under development
=============================================================

This describes the process and scripts Digital Campus has used to adapt content from the Open University (UK), for 
example the HEAT and OpenWASH content.

This content is already very well structured and edited, however there are a few areas that need to be updated so the 
courses display very well on OppiaMobile.

In terms of the ordering shown below, items 1 and 2 must be completed first, and there must always be a final quality 
assurance check, however the other items may be completed in any order or in parallel, since they are not dependent on 
each other.

1. Import courses to your Moodle server
---------------------------------------------

Import the Moodle course onto your own Moodle server - you will need to have full access to the Moodle installation and 
database for this adaptation.

2. Apply scripts
------------------
   
Updating and applying the scripts that we used for the HEAT content adaptation. These remove OU specific stylesheets and 
navigation. 
   
These scripts should be run in exactly this order, confirming succesful completion and expected results before running 
the next script. In Moodle you may need to purge the cache and/or save the course settings.
   
The scripts should be run from the command line - there is no user/web interface - and directly manipulate the Moodle 
database. They ought to work for all versions of Moodle v2.4.x - v2.9.x.

Firstly make a copy of `settings.php` named `local_settings.php` and update the information for your Moodle instance.
   
#. 01-restructure-course.php - the original Moodle courses have all the activities in a single Moodle topic. This 
   script uses the activity numbering to determine which section a course will appear in.
#. 02-order-topics.php - 
#. 03-clean-course.php - 



3. Apply styles
-------------------

Apply more general stylesheet, for example for the in-text questions, notes, warnings - using the same icons etc used 
for the mobile adapted HEAT content.

Refer to `helper/cleaning.php`

   
4. Review of image and table content
-----------------------------------------

Review of images and tables - to ensure they are resized/styled appropriately for display on mobile


5. Add activity icons/images
------------------------------------

Adding activity icons/images


6. Adapt SAQs into Moodle quiz format
-------------------------------------------

Adapt SAQs into Moodle quiz format - not all SAQ questions may be able to be adapted (depends on the complexity and 
type of question)


7. Quality Assurance and Review
-----------------------------------

QA check and review - the QA will focus on the layout/consistency of stylesheets/images/tables etc, but will not look at 
the actual content, spelling/grammar etc (as assume has already been very well reviewed for these aspects)
   
   
Appendix - Additional Helper Scripts
------------------------------------

