# oppia/reports/signals.py
from django.dispatch import Signal

import oppia
from reports.models import DashboardAccessLog

dashboard_accessed = Signal(providing_args=["request", "data"])


def dashboard_accessed_callback(sender, **kwargs):
    request = kwargs.get('request')
    data = kwargs.get('data')

    dal = DashboardAccessLog()
    dal.user = request.user
    dal.url = request.build_absolute_uri()
    dal.data = data
    dal.ip = request.META.get('REMOTE_ADDR', oppia.DEFAULT_IP_ADDRESS)
    dal.agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    dal.save()

    return

dashboard_accessed.connect(dashboard_accessed_callback)
