# oppia/reports/signals.py

from django.dispatch import Signal

from oppia.reports.models import DashboardAccessLog

dashboard_accessed = Signal(providing_args=["request", "data"])


def dashboard_accessed_callback(sender, **kwargs):
    request = kwargs.get('request')
    data = kwargs.get('data')

    print request.user
    print request.build_absolute_uri()
    
    dal = DashboardAccessLog()
    dal.user = request.user
    dal.url = request.build_absolute_uri()
    dal.data = data
    dal.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    dal.agent = request.META.get('HTTP_USER_AGENT','unknown')
    dal.save()
    
    return




dashboard_accessed.connect(dashboard_accessed_callback)