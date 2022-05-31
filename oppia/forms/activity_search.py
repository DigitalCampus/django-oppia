# oppia/profile/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.utils.translation import gettext as _

from helpers.forms.dates import DateRangeForm
from profile.forms import helpers

CUSTOMFIELDS_SEARCH_PREFIX = 'userprofilecustomfield_'


class ActivitySearchForm(DateRangeForm):
    user__username = forms.CharField(max_length=100, min_length=2, required=False, label=_('Username'))
    digest = forms.CharField(max_length=100, min_length=2, required=False, label=_('Activity digest'))
    type = forms.CharField(max_length=50, min_length=2, required=False, label=_('Activity type'))

    def __init__(self, *args, **kwargs):
        super().__init__(* args, ** kwargs)

        helpers.custom_fields(self,
                              prefix=CUSTOMFIELDS_SEARCH_PREFIX,
                              make_required=False)

        self.advanced = FormHelper()
        self.advanced.form_class = 'form-horizontal'
        self.advanced.label_class = ("col-sm-3 col-md-2 col-lg-2 pr-0 control-label")
        self.advanced.field_class = 'col-sm-8 col-md-4 col-lg-5'
        self.advanced.form_method = 'GET'
        self.advanced.layout = Layout()
        self.advanced.form_tag = False
        self.helper.form_tag = False

        self.advanced.layout.append(
            Div(
                Submit('submit', _('Search'), css_class='btn btn-default'),
                css_class='col-lg-7 col-md-7 col-sm-11 text-right',
            )
        )
