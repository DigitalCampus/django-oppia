# oppia/api/validation.py
from django.utils.translation import ugettext_lazy as _

from oppia.models import Activity, Media

from tastypie.validation import Validation

class TrackerValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        try:
            Activity.objects.get(digest=bundle.obj.digest)
        except Activity.DoesNotExist:
            pass

        try:
            Media.objects.get(digest=bundle.obj.digest)
        except Media.DoesNotExist:
            pass
        
        return errors
