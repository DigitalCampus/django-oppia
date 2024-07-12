import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-oppia',
    version='0.15.2',
    packages=[
        'oppia',
        'quiz',
        'profile',
        'content',
        'av',
        'settings',
        'summary',
        'reports',
        'activitylog',
        'viz',
        'gamification',
        'helpers'
    ],
    include_package_data=True,
    license='GNU GPL v3 License',  # example license
    description='Server side component of OppiaMobile learning platform',
    long_description=README,
    url='https://digital-campus.org/',
    author='Alex Little, Digital Campus',
    author_email='alex@digital-campus.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "django == 4.2.14",
        "django-tastypie == 0.14.6",
        "tablib == 3.6.0",
        "django-crispy-forms == 1.14.0",
        "pytz",
        "defusedxml==0.7.1",
        "Pillow==10.3.0",
        "sorl-thumbnail==12.10.0",
        "pycodestyle",
        "pytest",
        "pytest-django",
        "django-ses==3.5.2",
        "openpyxl==3.1.2",
        "reportlab==3.6.13",
        "django-compressor==4.4.0",
        "httpretty==1.1.4",
        "django-sass-processor==1.4",
        "qrcode==7.4.2",
        "libsass==0.23.0",
        "xmltodict==0.13.0",
        "django-storages==1.14.2",
        "django-database-view==0.3.0",
        "djangorestframework==3.15.2",
        "django-filter==23.5"
    ],
)
