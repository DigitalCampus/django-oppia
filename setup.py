import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-oppia',
    version='0.1.34',
    packages=['oppia','oppia.quiz','oppia.api','oppia.profile','oppia.quiz.api', 'oppia.migrations', 'oppia.quiz.migrations', 'oppia.mobile', 'oppia.fixtures'],
    include_package_data=True,
    license='GNU GPL v3 License',  # example license
    description='Server side component of OppiaMobile learning platform',
    long_description=README,
    url='http://oppia-mobile.org/',
    author='Alex Little, Digital Campus',
    author_email='alex@digital-campus.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "Django >= 1.5",
        "south >= 0.8.1",
	    "django-tastypie >= 0.9.16",
    ],
)
