################
Design/Layout
################



For changes to the design/layout such as changing the logo in the header, colour
scheme etc., this should be fairly straightforward and you should look at the 
following files in which to make these changes:

App icons and colors
--------------------

To use a different logo for your app, place your app logo in the drawable folder and update the following:

* In ``AndroidManifest.xml`` update ``android:icon="@drawable/dc_logo"`` to point to your logo (eg @drawable/my_logo)
* In ``org.digitalcampus.mobile.learning.application.MobileLearning`` class update ``public static final int APP_LOGO = 
  R.drawable.dc_logo;`` to point to you logo (eg R.drawable.my_logo)

To create this icon, you can rely on the Image Asset Studio tool that comes bundled with Android Studio to generate all 
the necessary images in its density-specific folder. To use it, just select right-click in the `res` folder of your project 
and select **New** > **Image Asset**. It will help you to create a Material design style icon based on your own 
image, and to generate the drawable in all the needed resolutions.

Another image that contains the OppiaMobile logo is the one representing the default course icon for the courses that 
don't include a custom one. If you want to change this, you have to replace the drawable ``default_course.png`` with the 
one you want. The general style for most of the courses in Oppia is to use a circle with a thin line border, so using an 
image following that guideline will fit better. 

If you want to go further with this customization, you can also change the default activity images with custom ones, for 
example to make them tinted to your brand color. This images are inside the drawables folder, named 
``default_icon_activity.png`` and ``default_icon_quiz.png``.

Colors
^^^^^^^

If you want to change the default green palette of the app to another set of colors that match better with your brand, 
you can do it so by simply changing the ``colors_oppia.xml`` values resource. You can deduce from their names where each 
color is used, but test the changes anyway until you acomplished the expected results.

Drawer design
---------------

You can change the design of the drawer menu as well, as it also contains the OppiaMobile logo and some green background.

The colors of the selected option on the drawer and the icons depend on the app colors (the ``colorPrimary`` value of 
the style, and ``highlight_light`` in the colors resource), so once you have changed that it will apply automatically to 
the drawer. The other thing you might want to modify is the drawer header design to use something more in line with your 
brand.

To modify the header, open the ``drawer_header.xml`` file under the layout resources folder. There, first of all you can 
change the main image that appears as the logo, changing the ``"source"`` parameter in the ``ImageView``, that by 
default uses the ``dc_logo`` drawable. We recommend using a squared image for this one, and something that has some 
contrast with the background. 

If the drawer background doesn't fit with your brand image, you can change that also. To do that, replace the 
``drawer_header_bg`` drawable in your res folder with another image of your choice. This image can have the resolution 
you want, but keep in mind that it will be cropped to fill the header space if the aspect ratio is different from its 
container, so it is recommended to use an horizontal image with a similar aspect ratio as the existing one.

Also, once you have change your background, if the image you chose is too dark the text may be hard to read. If this is 
your case, you can try changing the text color of some of the TextViews to a lighter one.



For more significant changes to the interface over and above changing the basic 
colour scheme and header etc, then this will require more substantial updates 
and familiarity with the code base.