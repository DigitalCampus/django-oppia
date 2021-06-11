import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-oppia',
    version='0.12.18',
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "django == 2.2.24",
        "django-tastypie == 0.14.2",
        "tablib == 3.0.0",
        "django-crispy-forms == 1.11.2",
        "pytz",
        "defusedxml==0.5.0",
        "Pillow==8.2.0",
        "sorl-thumbnail==12.7.0",
        "pycodestyle",
        "pytest",
        "pytest-django",
        "django-ses",
        "openpyxl==3.0.7",
        "reportlab==3.5.67",
        "django-compressor==2.4.1",
        "httpretty==1.1.1",
        "django-sass-processor==1.0.1",
        "qrcode==6.1"
    ],
)
