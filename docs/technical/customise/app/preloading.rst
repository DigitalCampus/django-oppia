Preloading Courses
=========================


If you would like to distribute your app with some courses preinstalled, for 
example if you have a lot of phones you would like set up with the same set of 
courses, then follow these steps:

* Place the course zip file(s) in the ``assets/www/preload/courses/`` directory
* Add the following lines to the ``doInBackground`` method of 
  ``org.digitalcampus.oppia.task.UpgradeManagerTask``::

		if(!prefs.getBoolean("upgradeVXXX",false)){
			Editor editor = prefs.edit();
			editor.putBoolean("upgradeVXXX", true);
			editor.commit();
			publishProgress("Upgraded to vXXX");
			payload.setResult(true);
		}

  where ``XXX`` is the new version number. The first time the app is installed 
  and run, the courses will be automatically installed.
  
* To subsequently distribute an updated version of the app (with new versions of
  the courses), then you will need to add another code block (with new version 
  number) to trigger the automatic installation of the updated/new courses.