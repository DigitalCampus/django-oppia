# oppia/activitylog/forms.py

from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Field

from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class UploadActivityLogForm(forms.Form):
    activity_log_file = forms.FileField(
                help_text=_(u'File types accepted: %s' % ', '.join(settings.OPPIA_UPLOAD_TRACKER_FILE_TYPES)),
                required=True,
                label=_(u'Activity Log'),
                error_messages={'required': _(u'Please select an activity log file to upload')},
                )

    def __init__(self, *args, **kwargs):
        super(UploadActivityLogForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('oppia_activitylog_upload')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'activity_log_file',
                Div(
                   Submit('submit', _(u'Upload'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )

    def clean(self):
        cleaned_data = super(UploadActivityLogForm, self).clean()
        activity_log_file = cleaned_data.get("activity_log_file")

        if activity_log_file is not None and activity_log_file.content_type not in settings.OPPIA_UPLOAD_TRACKER_FILE_TYPES:
            raise forms.ValidationError(_(u"You may only upload an activity log file which is one of the following types: %s" % ', '.join(settings.OPPIA_UPLOAD_TRACKER_FILE_TYPES)))
