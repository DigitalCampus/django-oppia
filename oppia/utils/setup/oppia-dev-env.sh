#!/bin/bash

DEV_ROOT=$PWD

echo "The current working directory: $PWD"

read -p "Project Name: " PROJ_NAME
read -p "MySQL admin username: " MYSQL_ROOT_USER
read -s -p "MySQL admin password: " MYSQL_ROOT_PW
echo -e "\n"

#create database & user
mysql -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PW -e 'CREATE DATABASE IF NOT EXISTS 'oppia_$PROJ_NAME' COLLATE 'utf8_general_ci';'
mysql -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PW -e 'GRANT ALL ON 'oppia_$PROJ_NAME'.* TO '$PROJ_NAME'@localhost IDENTIFIED BY "admin'$PROJ_NAME'"';
mysql -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PW -e 'flush privileges;'


#Start django project
django-admin startproject oppia_$PROJ_NAME

#create dirs
cd $DEV_ROOT/oppia_$PROJ_NAME
mkdir static
mkdir media
mkdir upload

#create virtual env
virtualenv $DEV_ROOT/oppia_$PROJ_NAME/env

#setup apps
cd $DEV_ROOT/oppia_$PROJ_NAME
source env/bin/activate

pip install django==1.6.6 south django-tastypie django-tablib django-crispy-forms mysql-python

deactivate

#set up urls.py
cp $DEV_ROOT/urls.py $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/urls.py

#set up settings.py
cp $DEV_ROOT/settings.py $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/settings.py
sed -i 's/<PROJ_NAME>/'$PROJ_NAME'/g' $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/settings.py
sed -i 's@<DEV_ROOT>@'$DEV_ROOT'@g' $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/settings.py

#set up wsgi.py
cp $DEV_ROOT/wsgi.py $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/wsgi.py
sed -i 's/<PROJ_NAME>/'$PROJ_NAME'/g' $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/wsgi.py
sed -i 's@<DEV_ROOT>@'$DEV_ROOT'@g' $DEV_ROOT/oppia_$PROJ_NAME/oppia_$PROJ_NAME/wsgi.py


#set up new apache conf file
sudo cp $DEV_ROOT/oppia-apache2.conf /etc/apache2/sites-available/oppia-$PROJ_NAME.conf
sudo sed -i 's/<PROJ_NAME>/'$PROJ_NAME'/g'  /etc/apache2/sites-available/oppia-$PROJ_NAME.conf
sudo sed -i 's@<DEV_ROOT>@'$DEV_ROOT'@g'  /etc/apache2/sites-available/oppia-$PROJ_NAME.conf

sudo a2ensite oppia-$PROJ_NAME.conf
sudo service apache2 restart

# update hosts
sudo sh -c " echo '127.0.0.1	localhost.oppia-"$PROJ_NAME"' >> /etc/hosts"

# clone git repos
git clone https://github.com/DigitalCampus/django-oppia.git $DEV_ROOT/django-$PROJ_NAME-oppia
git clone https://github.com/DigitalCampus/oppia-mobile-android.git $DEV_ROOT/$PROJ_NAME-oppia-mobile

cd $DEV_ROOT/oppia_$PROJ_NAME
source env/bin/activate
# collect static
python manage.py collectstatic

# create db
python manage.py syncdb

python manage.py migrate tastypie 
python manage.py migrate oppia
python manage.py migrate oppia.quiz 
python manage.py migrate oppia.viz

deactivate

echo "$PROJ_NAME is now set up"


