Creating own version of OppiaMobile app
================================================================

Time: 

Objectives
-------------


Activities
-------------


Code changes that need to be made:

Update the package attribute on manifest tag in AndroidManifest.xml (keeping with the 'reverse url' type notation), so 
for example, replace `org.digitalcampus.mobile.learning` with `org.myorgname.myproject.oppia`

Replace all instances of `import org.digitalcampus.mobile.learning.R;` with `import org.myorgname.myproject.oppia.R;`

Update the `MINT_API_KEY` in application/MobileLearning.java to the specific key you have generated for your app.




Follow up and preparation for next session
-------------------------------------------------------