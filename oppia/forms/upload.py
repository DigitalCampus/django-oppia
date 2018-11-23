import math

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from settings import constants
from settings.models import SettingProperties


class UploadCourseStep1Form(forms.Form):
    course_file = forms.FileField(
                required=True,
                error_messages={'required': _('Please select a file to upload')}, )

    def __init__(self, *args, **kwargs):
        super(UploadCourseStep1Form, self).__init__( * args, ** kwargs)

        max_upload = SettingProperties.get_int(constants.MAX_UPLOAD_SIZE, settings.OPPIA_MAX_UPLOAD_SIZE)
        self.fields['course_file'].help_text = _('Max size %(size)d Mb') % {'size': int(math.floor(max_upload / 1024 / 1024))}

        self.helper = FormHelper()
        self.helper.form_action = reverse('oppia_upload')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'course_file',
                Div(
                   Submit('submit', _(u'Upload'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )

    def clean(self):
        cleaned_data = super(UploadCourseStep1Form, self).clean()
        file = cleaned_data.get("course_file")

        max_upload = SettingProperties.get_int(constants.MAX_UPLOAD_SIZE, settings.OPPIA_MAX_UPLOAD_SIZE)

        if file is not None and file._size > max_upload:
            size = int(math.floor(max_upload / 1024 / 1024))
            raise forms.ValidationError(_("Your file is larger than the maximum allowed (%(size)d Mb). You may want to check your course for large includes, such as images etc.") % {'size': size, })

        if file is not None and file.content_type != 'application/zip' and file.content_type != 'application/x-zip-compressed':
            raise forms.ValidationError(_("You may only upload a zip file"))

        return cleaned_data


class UploadCourseStep2Form(forms.Form):
    tags = forms.CharField(
                help_text=_("A comma separated list of tags to help classify your course"),
                required=True,
                error_messages={'required': _('Please enter at least one tag')}, )
    is_draft = forms.BooleanField(
                help_text=_("Whether this course is only a draft"),
                required=False, )

    def __init__(self, *args, **kwargs):
        super(UploadCourseStep2Form, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'tags',
                'is_draft',
                Div(
                   Submit('submit', _(u'Save'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )
