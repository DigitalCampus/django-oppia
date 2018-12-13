REST API
========

This page describes the various REST API methods that may be called, what 
inputs/outputs they will accept/provide.

For almost all the API methods you will need to supply a ``username`` and 
``api_key`` (either as ``post`` or ``get`` parameters) otherwise you will get an
``HTTP 401 Unauthorized`` response

It is quite unlikely you will need to access these methods directly yourself, 
since the OppiaMobile client app handles all the API calls already.

By default all the methods will return JSON object(s).

Awards
------
Gets all the badges which have been awarded to the given user.

* Available methods: GET

* Required parameters:

	* ``username``
	* ``api_key``
	
* Example GET request::

 	http://localhost/api/v1/awards/?format=json&username=XXXX&api_key=XXXXXXXX
 

	
Badges
------
Gets all the badges that are currently available on the server.

* Available methods: GET

* Required parameters:

	* ``username``
	* ``api_key``
	
* Example GET request:: 

	http://localhost/api/v1/badges/?format=json&username=XXXX&api_key=XXXXXXXX

Course
------
Gets all the courses currently available on the server, and includes the link to
 download the course zip file

* Available methods: GET

* Required parameters:

	* ``username``
	* ``api_key``
	
* Example GET request:: 

	http://localhost/api/v1/course/?format=json&username=XXXX&api_key=XXXXXXXX
	
	
* Example GET request for downloading course zip file (also needs the required 
  parameters username and api_key)::

	http://localhost/api/v1/course/1/download/?username=XXXX&api_key=XXXXXXXX

Points
------
Gets all the points for the given user

* Available methods: GET

* Required parameters:

	* ``username``
	* ``api_key``
	
* Example GET request:: 

	http://localhost/api/v1/points/?format=json&username=XXXX&api_key=XXXXXXXX
	

Question
--------
For creating or returning a quiz question

* Available methods: GET, POST
* Required parameters (for both GET and POST requests):

	* ``username``
	* ``api_key``

* POST parameters:

	* ``title``  - required
	* ``type`` - required
	* ``responses`` - required, though may contain an empty set
	* ``props`` - optional set of properies
	
* Example GET request::

	http://localhost/api/v1/question/59/?format=json&username=XXXX&api_key=XXXXXXXX

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X POST --data '{"title":"A woman has sexual 
		intercourse with a man who is HIV-positive. She is tested for HIV 
		infection two weeks after this sexual intercourse. Her HIV test is 
		negative. Should you trust this result?","type":"multichoice",
		"responses":[],"props":[{"name":"maxscore","value":"1.0000000"}]}' 
		"http://localhost/api/v1/question/?username=XXXX&api_key=XXXXXXXX"

Quiz
----
For creating or returning a quiz 

* Available methods: GET, POST
* Required parameters (for both GET and POST requests):

	* ``username``
	* ``api_key``

* POST parameters:

	* ``title``  - required
	* ``description`` - required
	* ``questions`` - required, though may contain an empty set
	* ``props`` - required, though may contain an empty set

* Example GET request::

	http://localhost/api/v1/quiz/59/?format=json&username=XXXX&api_key=XXXXXXXX

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X POST --data '{"title":"ANC 4 SAQs","description":
		"Hormonal Regulation of the Female Reproductive System","questions":[],
		"props":[]}' "http://localhost/api/v1/quiz/?username=XXXX&api_key=XXXXXXXX"

QuizAttempt
-----------

For posting a quiz attempt 

* Available methods: POST
* Parameters (all required):

	* ``username``
	* ``api_key``
	* ``quiz_id`` 
	* ``maxscore``
	* ``score``
	* ``attempt_date``
	* ``responses`` - a set of responses (for each question)

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X POST --data '{"quiz_id":"27","maxscore":30,"score": 
		10,"attempt_date":"2012-12-18T15:35:12","responses":[{"question_id":"409", 
		"score":0,"text":"Orlando"},{"question_id":"410","score":0,"text": 
		"Jacksonville beaches"},{"question_id":"411","score":10,"text":"Dade  
		County"}]}'  
		"http://localhost/api/v1/quizattempt/?username=XXXX&api_key=XXXXXXXX"
 

QuizProps
---------

For creating or returning quiz properties. Usually used to add a ``digest`` 
property for the quiz. 

* Available methods: GET, POST
* Required parameters (for both GET and POST requests):

	* ``username``
	* ``api_key``

* POST parameters:

	* ``name``  - required
	* ``value`` - required
	* ``quiz`` - required - URI reference to the quiz

* Example GET request::

	http://localhost/api/v1/quizprops/10aa48109651ee7f45af789c382131a4/?format=json&username=XXXX&api_key=XXXXXXXX

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X  POST --data '{"name":"digest","value":
		"10aa48109651ee7f45af789c382131a4", "quiz":"/api/v1/quiz/636/"}' 
		"http://localhost/api/v1/quizprops/?username=XXXX&api_key=XXXXXXXX"
	

QuizQuestion
------------

For adding a question to a quiz

* Available methods: GET, POST
* Required parameters (for both GET and POST requests):

	* ``username``
	* ``api_key``

* POST parameters:

	* ``quiz`` - required - resource_uri to the quiz (will have been returned 
	  when the quiz was created)
	* ``question`` - required - resource_uri to the question (will have been 
	  returned when the question was created)
	* ``order`` - required 

* Example GET request::

	http://localhost/api/v1/quizquestion/1621/?format=json&username=XXXX&api_key=XXXXXXXX

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X  POST --data '{"question":
		"/api/v1/question/1824/", "quiz":"/api/v1/quiz/356/", 
		"order":"5"}'
		 "http://localhost/api/v1/quizquestion/?username=XXXX&api_key=XXXXXXXX"
		
Register
--------

For user registration (obviously no api_key required)

* Available methods: POST

* Parameters (all required):

	* ``username``
	* ``password``
	* ``passwordagain``
	* ``email``
	* ``firstname``
	* ``lastname``

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X POST --data '{"username":"demo","password":
		"mypassword", "email":"demo@myemail.com","passwordagain":"mypassword",
		"firstname":"demo","lastname":"user"}' 
		http://localhost/api/v1/register/

* POST request will return a JSON object in the following format::

	{
		"api_key": "9fa50a5e49cce4d0a5ab89c6c21faec284630e7b", 
		"badges": 0,
		"email": "demo@myemail.com", 
		"first_name": "demo", 
		"last_name": "user", 
		"points": 100, 
		"username": "demo"
	}
		 
Response
--------
For adding a possible response to a quiz question

* Available methods: GET, POST
* Required parameters (for both GET and POST requests):

	* ``username``
	* ``api_key``

* POST parameters:

	* ``question`` - required - resource_uri to the question (will have been 
	  returned when the question was created)
	* ``order`` - required 
	* ``title`` - required 
	* ``score`` - required 
	* ``props`` - optional

* Example GET request::

	http://localhost/api/v1/response/4050/?format=json&username=XXXX&api_key=XXXXXXXX

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X  POST --data 
		'{"question":"/api/v1/question/1829/","title":"my response", 
		"order":5, "score":10, "props":[{"name":"feedback","value":"Correct, 
		well done!"}]}' 
		"http://localhost/api/v1/response/?username=XXXX&api_key=XXXXXXXX"
		
Tag
---
For getting the tags and number of courses for each tag

* Available methods: GET
* Required parameters:

	* ``username``
	* ``api_key``

* Example GET request (for getting the set of tags)::

	http://localhost/api/v1/tag/?format=json&username=XXXX&api_key=XXXXXXXX
 
* Example GET request (for getting the courses tagged with tag_id 2)::

	http://localhost/api/v1/tag/2/?format=json&username=XXXX&api_key=XXXXXXXX
	
Tracker
-------

For submitting a track of an activity

* Available methods: POST
* Parameters:

	* ``username`` - required
	* ``api_key`` - required
	* ``digest`` - required 
	* ``data`` - optional - a JSON object of additional data to store along with
	  this tracker object
	* ``completed`` - optional - 0 or 1 (defaults to 0)

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X POST --data '{"digest":
		"ddeee1c1eec4f842b8b704dbd5889dcc","data":"{}","completed":1}' 
		"http://localhost/api/v1/tracker/?username=XXXX&api_key=XXXXXXXX"

* POST request will return a JSON object in the following format::

	{
		"badges": 8, 
		"completed": false, 
		"data": "", 
		"digest": "ddeee1c1eec4f842b8b704dbd5889dcc", 
		"points": 656, 
		"resource_uri": "/api/v1/tracker/3912/", 
		"tracker_date": "2013-06-28T18:44:08.845329", 
		"user": "/api/v1/user/1/"
	}
			
User
----

For logging a user in

* Available methods: POST
* Parameters:

	* ``username`` - required
	* ``password`` - required

* Example CURL POST request::

	curl --dump-header - -H "Accept: application/json" -H "Content-Type: 
		application/json" -X POST --data '{"username":"myusername","password":
		"mypassword"}' "http://localhost/api/v1/user/"

* POST request will return a JSON object in the following format::

	{
		"api_key": "9fa50a5e49cce4d0a5ab89c6c21faec284630e7b", 
		"badges": 0, 
		"first_name": "demo", 
		"last_login": "2013-06-28T18:50:35.523539", 
		"last_name": "user", 
		"points": 100, 
		"resource_uri": "/api/v1/user/317/", 
		"username": "demo"
	}
