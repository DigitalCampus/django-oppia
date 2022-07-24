from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms
from django.utils.translation import gettext_lazy as _
from oppia import constants as OppiaConstants
from oppia.forms.upload import UploadCourseStep2Form
from oppia.models import CourseStatus


class EditCourseForm(UploadCourseStep2Form):

    status = forms.ChoiceField(
        choices=CourseStatus.get_available_statuses(),
        help_text=_(OppiaConstants.STATUS_FIELD_HELP_TEXT),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(* args, ** kwargs)
        self.helper.layout = Layout(
                'categories',
                'status',
                'restricted',
                Div(
                   Submit('submit', _(u'Save'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )
