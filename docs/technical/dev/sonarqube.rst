SonarQube Set Up
==================

There are different ways to 


https://coverage.readthedocs.io/en/latest/index.html

https://docs.sonarqube.org/display/PLUG/Python+Coverage+Results+Import


coverage erase
coverage run --branch --source=activitylog,api,av,content,gamification,oppia,profile,quiz,reports,summary,viz manage.py test
coverage xml -i

/sonar-scanner \
  -Dsonar.projectKey=<your-project-key> \
  -Dsonar.organization=<your-organisation> \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=<your-login-key> \
  -Dsonar.exclusions=docs/_build/**/* \
  -Dsonar.python.coverage.reportPath=./coverage.xml