SonarQube Set Up
==================

There are different ways to set up and use `SonarQube <https://www.sonarqube.org/>`_, 
it's an enterprise level product for analysing source code to maintain code 
quality.

OppiaMobile Server
------------------------

We use the `sonar-scanner <https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner>`_ 
tool on the command line to analyse the Oppia server source code and submit the 
results to `SonarCloud <https://sonarcloud.io/dashboard?id=django_oppia>`_.

First we create the test coverage report, using the `Coverage <https://coverage.readthedocs.io/en/latest/index.html>`_ 
tool, using::

	$ coverage erase
	$ coverage run --branch --source=activitylog,api,av,content,gamification,oppia,profile,quiz,reports,summary,viz manage.py test
	$ coverage xml -i
	
Then copy the generated ``django-oppia/coverage.xml`` file into the 
``django-oppia/tests/`` directory.

Then we run the sonar-scanner using::

	/sonar-scanner \
	  -Dsonar.projectKey=django_oppia \
	  -Dsonar.organization=alexlittle-github \
	  -Dsonar.sources=. \
	  -Dsonar.host.url=https://sonarcloud.io \
	  -Dsonar.login=be506baef7967f202dcb21d0feb1fb8cabf52478 \
	  -Dsonar.exclusions=docs/_build/**/*,tests/**/*,oppiamobile/settings_secret.py \
	  -Dsonar.python.coverage.reportPath=./tests/coverage.xml
	  
OppiaMobile Android App
------------------------

TODO: To be completed.