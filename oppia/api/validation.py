# oppia/api/validation.py
from django.utils.translation import ugettext_lazy as _

from oppia.models import Activity, Media

from tastypie.validation import Validation

class TrackerValidation(Validation):
    def is_valid(self, bundle, request=None):
        exists = False
        errors = {}
        try:
            activity = Activity.objects.get(digest=bundle.obj.digest)
            exists = True
        except Activity.DoesNotExist:
            pass
        
        try:
            media = Media.objects.get(digest=bundle.obj.digest)
            exists = True
        except Media.DoesNotExist:
            pass
        if not exists:
            pass
        return errors

