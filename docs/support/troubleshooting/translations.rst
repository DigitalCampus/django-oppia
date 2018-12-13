Troubleshooting Multilingual Content
=====================================

OppiaMobile uses the in-built Moodle functionality for authoring courses in multiple languages.

For troubleshooting translations it is best to start trying to fix a single page, and ensuring that when the page is 
displayed in Moodle, the language switching is working correctly. If the language switching is not working in Moodle, 
then it will not work when the course is exported to Oppia either.

The `Moodle documentation <http://docs.moodle.org/en/Multi_language_content>`_ has some information on how to 
fix common problems. 

Additional problems we have noticed:


Using mismatching single or double quotes
-------------------------------------------

Be careful to check that the single or double quotes in the HTML tags are of matching types. In the examples 
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
size selected. Here is an example of mismatching quotes in the Moodle inline HTML editor:

.. image:: images/moodle-editor-incorrect-html.png

The likely cause of having different types of quotes is from cutting and pasting from different sources.


Additional style attribute used in page and topic titles
---------------------------------------------------------

For page and topic/section titles, when the multilang span tags include additional attributes, this seems to stop the 
Moodle multilang filter functioning correctly, but applies to the titles only, not the page content.

Example 1 (does not work):

.. code:: 
	
	<span lang="ur" class="multilang" style="font-size: 1rem;">ويڊيو جو خلاصو</span><span lang="ar" class="multilang" style="font-size: 1rem;">ايپليڪيشن جو تعارف</span>

Example 2 (does work):

.. code:: 
    
    <span lang="ur" class="multilang">ويڊيو جو خلاصو</span><span lang="ar" class="multilang">ايپليڪيشن جو تعارف</span>
	
The difference being that the ``style="font-size: 1rem;"`` attribute has been removed.




