Multilingual Interface and Content in the OppiaMobile App
===========================================================

For translating OppiaMobile, there are two separate areas to consider, the app 
interface and the course content.

App Interface
---------------

The language that the OppiaMobile app interface appears in (e.g. the buttons, 
menu items etc), is determined by translation files directly included and 
compiled into the app. Which language file is used is determined by the language
that the whole phone interface is set to. This will default to English if the 
phone is set to a language that Oppia does not have a language file for.

To add a new interface language:

* Make copy of ``strings.xml`` from 
  https://github.com/DigitalCampus/oppia-mobile-android/blob/master/res/values/strings.xml
* Translate the English text (just the value, not the string name attribute).
* Create a new directory in the ``res`` directory called ``values-XX`` - where 
  XX is the language code for the translation
* Copy the new ``strings.xml`` file into this new directory



Course Content
---------------

Providing translations of course content is completely separate from the 
application interface. This means that users can select which language they 
would like to view the course content in, but without needing to change the 
phone interface language.

When the app is first installed, the course language setting will default to the 
phone settings language. If a course isn't provided in the phone setting 
language, then it will default to the first language the course is provided in.

To create a course in multiple languages, when you are writing the course, just 
use the usual Moodle method for providing multilingual courses. You can find 
more information about this at: http://docs.moodle.org/en/Multi_language_content

When the course is exported to OppiaMobile, it will then allow users to switch 
between languages in the OppiaMobile app.

