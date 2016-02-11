Installing VirtualBox Image
=================================

As well as the Amazon Web Services Machine Image, we also have a VirtualBox 
image of a new/clean installation of the OppiaMobile Server.

The latest version is available to download from: 
http://downloads.digital-campus.org/OppiaMobile/virtualbox-images/

The configuration is all set up with the same directory structure, passwords etc 
as on the AWS image, so you can find :ref:`all the details here <aws>`.

The only additional information you should need is the user login account:

* username: oppia
* password: default

Obviously as soon as you have installed the machine you should change this to 
something much more secure.

Downloading the Virtual Machine Images
--------------------------------------
The VirtualBox images are large files (2Gb+) so may take a long time to 
download. To help those of you on slow connections, we have made the latest 
Virtual Machine Image available to download by using BitTorrent Sync 
(http://www.bittorrent.com/sync), using the read-only key 
``BI2VPY62BTBZ6K7C764KZCOAVDA2IJEET``. 

Environment information
-----------------------
The current version of the instance is running:

* Ubuntu 14.04 LTS Desktop
* Apache 2.4
* Mysql 5.5
* Django 1.8.5
* TastyPie 0.12.1
* OppiaServer 0.9.2