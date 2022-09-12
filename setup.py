import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-oppia',
    version='0.14.2',
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
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "django == 3.2.15",
        "django-tastypie == 0.14.4",
        "tablib == 3.2.1",
        "django-crispy-forms == 1.14.0",
        "pytz",
        "defusedxml==0.7.1",
        "Pillow==9.2.0",
        "sorl-thumbnail==12.9.0",
        "pycodestyle",
        "pytest",
        "pytest-django",
        "django-ses==3.1.2",
        "openpyxl==3.0.10",
        "reportlab==3.6.11",
        "django-compressor==4.1",
        "httpretty==1.1.4",
        "django-sass-processor==1.2.1",
        "qrcode==7.3.1",
        "libsass==0.21.0",
        "xmltodict==0.13.0",
        "django-storages==1.13.1",
        "django-database-view==0.3.0"
    ],
)
