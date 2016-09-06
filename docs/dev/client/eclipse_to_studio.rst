Migrating Android repository from Eclipse ADT to Android Studio
==================================================================

By the end of 2015, Google ended the development and official support for the Android Developer Tools (ADT) in Eclipse. 
This specifically includes the Eclipse ADT plugin, with which the OppiaMobile Android app was developed. As stated by 
Google, every app development project should be migrated to Android Studio as soon as possible. 

It introduces some changes in terminology that need to be clarified:

* **Project:** A project in *Android Studio* is like a **workspace** in *Eclipse*. This would be entire project context. 
  Whatever you do in Android Studio, you do that in the context of a project. A project is an organizational unit that 
  represents a complete software solution. In fact, if you want to work in more than one app, you'll have to work in 
  different instances of *Android Studio*.

* **Module:** A module in *Android Studio* is like a **project** in *Eclipse*. Each project has at least an `app` module 
  that contains the main application source code, resource files, and application level settings, such as the 
  module-level build file, resource files, and Android Manifest file.

* **Dependencies:** The biggest change is the use of **Gradle** to configure and build the project. Instead of having 
  library projects in the workspace, we define every dependency in our gradle files. The biggest advantage is the 
  possibility to add remote dependencies to the project as we will see later.

To learn more about Android Studio, see the overview in the Android Developers page: 
https://developer.android.com/tools/studio/index.html

Project structure
---------------------

The biggest barrier to migrate to Android Studio is that the folder structure of the project is different, so it can be 
dangerous to the Git file history. To see the differences, lets have a look side by side to Eclipse and Android Studio 
project structure.

Eclipse::

	oppiamobile/
	   |_ assets
	   |_ bin (hidden by .gitignore)
	   |_ gen (hidden by .gitignore) 
	   |_ libs
	   |_ res
	   |     |_ anim
	   |     |_ drawable
	   |     |_ ... etc
	   |_ src
	   |     |_ org/digitalcampus/oppia....
	   |_ .gitignore
	   |_ AndroidManifest.xml
	   |_ build.xml
	   |_ project.properties
	   |_ README.md


Android Studio::

	oppiamobile/
	   |_ app
	   |     |_ build (hidden by .gitignore)
	   |     |_ libs
	   |     |_ src
	   |     |     |_ test  --> to implement unit testing
	   |     |     |_ main
	   |     |           |_ assets
	   |     |           |_ java
	   |     |           |    |_ org/digitalcampus/oppia...
	   |     |           |_ res
	   |     |           |     |_ anim
	   |     |           |     |_ drawable
	   |     |           |     |_ ... etc
	   |     |           |_ AndroidManifest.xml
	   |     |_ .gitignore
	   |     |_ build.gradle --> here we define project dependencies
	   |_ build.gradle --> here we define repositories and classpath dependencies
	   |_ settings.gradle --> here we include submodules (in our case, app)
	   |_ README.md


Migration process
-----------------------

Migrating from Eclipse ADT to Android Studio requires adapting to the new project structure and build system. To 
simplify the migration process, Android Studio provides an import tool so you can quickly transition your Eclipse ADT 
workspaces and Ant build scripts to Android Studio projects and Gradle-based build files. 

The problem: Git might identify these files as simply moved/renamed, but unfortunately that doesn't happen often, so the 
Git file history of all the source code of the project can get lost in the process. Instead, to prevent any issue, the 
best approach is to run the migration tool in a separate location and manually recreate the moves on the original 
repository. Now we describe how to perform this migration step by step:

1. Download and install Android Studio: http://developer.android.com/intl/es/sdk/index.html

2. Open Android Studio and select "Import project (Eclipse ADT, Gradle, ...). Select the root OppiaMobile repository 
   folder and then set a new destination for the import (for example, `temp-import`). It should take less than a minute 
   and import the project without issues.

3. Once your import is complete, Android Studio displays an import summary, describing all the changes it’s made to your 
   project. This summary contains details about which files were moved during the import process, and where you can find 
   them in the new Android Gradle layout, plus information on any third party libraries or JAR files that Android Studio 
   has replaced with Gradle dependencies.

4. By default, Android Studio searches for library equivalences with your current dependencies. If it doesn't find a 
   maven library, it will simply copy the jar file that was there before. If any of these libraries were not detected,
   replace manually with the following line(s):
    
    * `joda-time-2.2.jar`: `compile 'joda-time:joda-time:2.2'`
    * `androidplot-core-0.6.1.jar`: `compile "com.androidplot:androidplot-core:0.6.1"`
    * `picasso-2.5.2.jar`: `compile 'com.squareup.picasso:picasso:2.5.2'`
    * `okhttp-3.1.2.jar`: `compile 'com.squareup.okhttp3:okhttp:3.1.1'`
    * `mint-4.4.0.jar`: `compile "com.splunk.mint:mint:4.2"`
    
Once you change this dependencies with its Gradle equivalent and make sure that the project compiles, you can delete the 
related jar from the `/app/libs/` folder

5. Now it's time to apply the changes in the repository. First, create and checkout a new branch in the Eclipse project 
   location. This will make it easier to delete any changes if migration gets messy :)

6. Recreate the new source code structure, moving each file to where its new location will be. For Linux users, it can 
   be done by running these commands::

	mkdir -p app/src/main/java
	git mv src/com app/src/main/java
	git mv res app/src/main
	git mv assets app/src/main
	git mv AndroidManifest.xml app/src/main

Make sure that the files are detected as a move by using `git status` (not needed if using `git mv` command)

7. Copy all the gradle files from the temporary imported project into the repository. For Linux users, assuming that 
   both the repo directory and the temporary imported project directory are in the same folder, it can be done by 
   running these commands::

	cp temp-import/app/build.gradle oppia-mobile-android/app/
	cp -r temp-import/gradle oppia-mobile-android/
	cp temp-import/build.gradle oppia-mobile-android/
	cp temp-import/gradlew oppia-mobile-android/
	cp temp-import/gradlew.bat oppia-mobile-android/
	cp temp-import/settings.gradle oppia-mobile-android/


8. Edit the `.gitignore` file and add the new Android Studio files that can be ignored in the repository::

	/.idea/
	/build
	/app/build
	/gradle
	*.iml
	.gradle
	gradle.properties
	gradlew
	gradlew.bat


9. Finally, we can remove the old Eclipse files as they are no longer needed, remove the temporary project and open the 
   project with Android Studio. As we only copied the minimum possible from the other project, it will detect it at 
   first as a plain gradle project in the folder hierarchy selector, but once it scans the project it will mark it as 
   an Android project, generating all the IDE files associated (that we have added to the .gitignore file manually). 
   If everything is working properly, we can make the commit and start to get used to the new IDE :)