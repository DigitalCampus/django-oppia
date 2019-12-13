from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt


class XFrameOptionsExemptMixin(View):
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super(XFrameOptionsExemptMixin, self).dispatch(*args, **kwargs)
