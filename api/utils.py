from django.utils.translation import gettext_lazy as _

from tastypie.exceptions import BadRequest


def check_required_params(bundle, required):
    for r in required:
        try:
            bundle.data[r]
        except KeyError:
            raise BadRequest(_(u'Please enter your %s') % r)
