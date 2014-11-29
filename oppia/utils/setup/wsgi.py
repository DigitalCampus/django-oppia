"""
WSGI config for oppia_core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

path = '<DEV_ROOT>/oppia_<PROJ_NAME>/'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oppia_<PROJ_NAME>.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
