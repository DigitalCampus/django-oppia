import json
import oppia

from django.dispatch import Signal
from reports.models import DashboardAccessLog

dashboard_accessed = Signal(providing_args=["request", "data"])


def dashboard_accessed_callback(sender, **kwargs):
    request = kwargs.get('request')
    data = kwargs.get('data')

    if request.path.startswith("/admin") or request.path.startswith("/api"):
        return

    data_to_store = {}
    if data:
        for d in data:
            # don't save any sensitive info
            if d not in ('csrfmiddlewaretoken',
                         'password',
                         'password_again',
                         'api_key'):
                data_to_store[d] = data[d]

    if request.user.is_authenticated:
        dal = DashboardAccessLog()
        dal.user = request.user
        dal.url = request.path
        dal.data = json.dumps(data_to_store)
        dal.ip = request.META.get('REMOTE_ADDR', oppia.DEFAULT_IP_ADDRESS)
        dal.agent = request.META.get('HTTP_USER_AGENT', 'unknown')
        dal.save()


dashboard_accessed.connect(dashboard_accessed_callback)
