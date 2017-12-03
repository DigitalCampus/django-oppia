Troubleshooting Multilingual Content
=====================================

OppiaMobile uses the in-built Moodle functionality for authoring courses in multiple languages.

For troubleshooting translations it is best to start trying to fix a single page, and ensuring that when the page is 
displayed in Moodle, the language switching is working correctly. If the language switching is not working in Moodle, 
then it will not work when the course is exported to Oppia either.

The `Moodle documentation <http://docs.moodle.org/en/Multi_language_content>`_ has some information on how to 
fix common problems. 

One additional problem we have noticed, is using mismatching single or double quotes in the HTML tags. In the examples 
below (shown as large image as well as plain text), the first example uses a different type of double quotes. The 
multilanguage filter in Moodle then cannot understand what is meant by the HTML code, and so fails to recognise that we 
are trying to enter multilingual content. 

Example 1 (incorrect): 

.. image:: images/quotes-incorrect.png

.. code:: 

	class="multilang”

Example 2 (correct): 

.. image:: images/quotes-correct.png
	
.. code:: 

	class="multilang"
	
In the Moodle inline HTML editor, it is very difficult to see that different types of quotes have been used. It is much 
easier to notice if the page HTML is cut and pasted into a plain text editor (eg Notepad or similar) with a large font 
size selected.

The likely cause of having different types of quotes is from cutting and pasting from different sources.

