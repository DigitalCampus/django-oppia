Testing Process for OppiaMobile App
=====================================

*OppiaMobile* incorporates several types of tests to make the app stronger.

These types of tests are **Local Unit Tests**, **Instrumented Tests** and **User Interface Tests**.


Local Unit Tests
-------------------
The Local Unit Tests are tests that run on a local JVM, therefore we do not need a physical device or emulator to run this type of tests, which make the execution time to be shorter.

The main path for these tests is ``src/test/java``. It is mandatory for this type of tests to include the JUnit 4 framework dependency to the app *build.gradle* file.

.. code-block:: text

   testCompile 'junit:junit:4.12'
 
The tests methods that we create must have the tag ``@Test`` right before the method declaration, and must end with an **assertion** to check whether the test passes or not. For example:
 
.. code-block:: text

   @Test
   public void Storage_correctDownloadPath(){
	      …

	      assertTrue(downloadPath.isCorrect());
   }
 

Optionally, the tests could provide a preconditions and post conditions blocks

.. code-block:: text

 //Preconditions block

 @Before
 public void setUp() throws Exception{…}



.. code-block:: text

 //Preconditions block

 @Before
 public void setUp() throws Exception{…}


Instrumented Unit Tests
-------------------------

The Instrumented Unit Tests are test that run on a physical device or emulator. This type of tests is convenient when we need access to instrumentation information (App context for example).

The main path for this tests is ``src/androidTests/java``.

To create and run this test, first we need to install the **Android Support Repository** from the *Android SDK Manager*. After that, we need to add some dependencies to the app *build.gradle* file:

 
.. code-block:: XML

    androidTestCompile 'com.android.support:support-annotations:24.0.0'
    androidTestCompile 'com.android.support.test:runner:0.5'
    androidTestCompile 'com.android.support.test:rules:0.5'

In addition, we need to add the default test instrumentation runner to use JUnit 4 test classes:

.. code-block:: XML
 
 android {
     defaultConfig {
         testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
     }
 }

When we create a test class, there are some things we have to pay attention.

* We need to add the ``@RunWith(AndroidJUnit4.class)`` tag before the test class definition.
 
* We also need to add the ``@Test`` tag to all our test methods (as we did in the *Local Unit Tests* section) 
 
* The ``setUp()`` and ``tearDown()`` methods have the same structure as in the *Local Unit Tests* section.
 
* All our tests methods should include the **throws Exception** line in the method definition.
 
* The assertion part is the same as in the *Local Unit Tests* section.

User Interface Tests
-----------------------
 
The User Interface Tests are useful to verify that the UI components of the app works correctly and do not provide a poor experience to the final user.

*OppiaMobile* make use of these tests using the **Espresso** testing framework, that we might consider it as an Instrumentation-based framework to test UI components. 

With *Instrumentation-based* we mean that it works with the **AndroidJUnitRunner** test runner (as mention in the previous section).

To use the Espresso library, we need to make sure to follow the same steps described in the previous section (Instrumented Unit Tests) and also we need to add the following dependency to the app *build.gradle* file:


.. code-block:: XML
 
 androidTestCompile 'com.android.support.test.espresso:espresso-core:2.2.1'

.. note::
 It is recommended to turn off the animations on your test device (*Settings --> Developing Options*), as they might cause         unexpected results or may lead your test to fail.
 

There are some things we need to take into account:

* We need to specify at the beginning of the class the activity that will be tested. This is done with the **@Rule** tag and with a ``ActivityTestRule`` object:


 .. code-block:: java

  @Rule
  public ActivityTestRule<OppiaMobileActivity> oppiaMobileActivityTestRule = 
                                                            new ActivityTestRule<>(OppiaMobileActivity.class);
 

* The *Espresso* nomenclature is based on three aspects. First we need to **find the view** we want to test. Next, we have to **perform an action** over that view. And finally, we need to **inspect the result**. This is done as follows:

 .. code-block:: java

	  onView(withId(R.id.login_btn))		        //Find the view 
	          .perform(click());		            //Perform an action 
	  onView(withText(R.string.error_no_username))	//Find the view
		      .check(matches(isDisplayed()));       //Inspect the result

Mock Web Server
-----------------

*OppiaMobile* made use of the **MockWebServer** by *okhttp* (https://github.com/square/okhttp/tree/master/mockwebserver).

The mock web server is useful to enqueue some responses and in this way testing the client side.

First, we need to add the MockWebServer dependency to our app *build.gradle* file:

.. code-block:: XML
 
	 testCompile 'com.squareup.okhttp3:mockwebserver(insert latest version)’


After that, we are able to create MockWebServer objects. For example:



.. code-block:: text
 
	 MockWebServer mockServer = new MockWebServer();
	
	 String filename = “responses/response_201_login.json”; //Premade response
	
	 mockServer.enqueue(new MockResponse()
		    .setResponseCode(201)
	     	.setBody(getStringFromFile(InstrumentationRegistry.getContext(),
				                              filename)));
	
	 mockServer.start(); 


On the other hand, we need to configure our app to communicate correctly with this mock web server. To achieve that, *OppiaMobile* uses the class ``MockApiEndpoint``, whose method ``getFullURL()`` will give us the correct path on which the mock web server is listening.


Temporary Files and Folders
-----------------------------

**Junit4** allows us to create temporary files and folders with the guarantee that it will delete all of them when the test finishes, whether the test passes or fails.

The ``TemporaryFolder`` object must be created using the ``@Rule`` tag.

.. code-block:: text
 
	 @Rule 
	 public TemporaryFolder folder = new TemporaryFolder();
	
	 //Use
	 File tempFolder = folder.newFolder(“tempFolder”);
	 File tempFile = folder.newFile(“tempFile.txt”);


Running Tests
---------------

We have several ways to run tests:

* **Run a single test**:
 
 First, open the class where the test is located, and then right-click the test and click **Run**.

* **Run all tests in a class**:

 Right-click the class you want to test and click **Run**.

* **Run all tests classes in a directory**:

 Right-click the directory you want to test and click **Run tests**.

* **Run tests using a test suite**:

 A test suite allows us to run a collection of test that we want. 

 To create a test suite, we need to create a new class and add these tags to the beginning of it:

 .. code-block:: text
  
	  @RunWith(Suite.class)
	  @Suite.SuiteClasses({WelcomeUITest.class, LoginUITest.class, RegisterUITest.class, ResetUITest.class})
	
	  public class UITestSuite {…}


 If we run this suite, the tests inside in the classes listed in ``@Suite.SuiteClasses()`` will be executed.