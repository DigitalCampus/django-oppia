REST API
========

This page describes the various REST API methods that may be called, what input/ouput they will accept/provide.

For almost all the API methods you will need to supply a ``username`` and ``api_key`` (either as ``post`` or ``get`` parameters) otherwise you will get an ``HTTP 401 Unauthorized`` response

It is quite unlikely you will need to access these methods directly yourself, since the OppiaMobile client app handles all the API calls already.

By default all the methods will return JSON object(s).

Awards
------
Gets all the badges which have been awarded to the given user.

* Available methods: GET
* Example GET request: http://localhost/api/v1/awards/?format=json&username=XXXX&api_key=XXXXXXXX
* Required parameters:
	* username
	* api_key
	
Badges
------
Gets all the badges that are currently available on the server.

* Available methods: GET
* Example GET request: http://localhost/api/v1/badges/?format=json&username=XXXX&api_key=XXXXXXXX
* Required parameters:

	* username
	* api_key

Course
------
Gets all the courses currently available on the server, and includes the link to download the course zip file

* Available methods: GET
* Example GET request: http://localhost/api/v1/course/?format=json&username=XXXX&api_key=XXXXXXXX
* Required parameters:

	* username
	* api_key
	
* Example GET request for downloading course zip file (also needs the required parameters username and api_key):
	http://localhost/api/v1/course/1/download/?username=XXXX&api_key=XXXXXXXX

Points
------
Gets all the points for the given user

* Available methods: GET
* Example GET request: http://localhost/api/v1/points/?format=json&username=XXXX&api_key=XXXXXXXX
* Required parameters:

	* username
	* api_key
	
Question
--------
For creating or returning a quiz question

* Available methods: GET, POST
* Required parameters (for both GET and POST requests):

	* username
	* api_key

* Required POST parameters:

	* title
	* type
	* 
	
	
* Example GET request: http://localhost/api/v1/question/59/?format=json&username=XXXX&api_key=XXXXXXXX

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: application/json" -X POST --data '{"title":"A woman has sexual intercourse with a man who is HIV-positive. She is tested for HIV infection two weeks after this sexual intercourse. Her HIV test is negative. Should you trust this result?","type":"multichoice","responses":[],"props":[{"name":"maxscore","value":"1.0000000"}]}' "http://localhost/api/v1/question/?format=json&username=XXXX&api_key=XXXXXXXX"

Quiz
----

QuizAttempt
-----------

QuizProps
---------

QuizQuestion
------------

Register
--------

Response
--------


Schedule
--------

Scorecard
---------

Tag
---

Tracker
-------

User
----

