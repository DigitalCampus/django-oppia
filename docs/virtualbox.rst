Installing VirtualBox Image
=================================

As well as the Amazon Web Services Machine Image, we also have a VirtualBox 
image of an new installation of the OppiaMobile Server.

The latest version is available to download from: 
http://downloads.digital-campus.org/OppiaMobile/virtualbox-images/

The configuration is all set up with the same directory structure, passwords etc 
as on the AWS image, so you can find :ref:`all the details here <aws>`.

The only additional information you should need is the user login account:

* username: oppia
* password: default

Obviously as soon as you have installed the machine you should change this to 
something much more secure.

Environment information
-----------------------
The current version of the instance (OppiaMobile Server 0.4.0) is running:

* Ubuntu 12.04 LTS Desktop
* Apache 2
* Mysql 5.5
* Django 1.6.1
* TastyPie 0.11.0
* South 0.8.4
* OppiaServer 0.4.0