# oppia/av/forms.py

from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Field

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class UploadMediaForm(forms.Form):
    media_file = forms.FileField(
                help_text=_('Media file types accepted: %s' % ', '.join(settings.OPPIA_MEDIA_FILE_TYPES)),
                required=True,
                error_messages={'required': _('Please select a media file to upload')},
                )
    media_image = forms.FileField(
                help_text=_('Select an image file for this media, types accepted: %s' % ', '.join(settings.OPPIA_MEDIA_IMAGE_FILE_TYPES)),
                required=False,
                )
    course_shortname = forms.CharField( 
                help_text=_("Short name of the course this media file is linked to"),
                required=False)
    length = forms.IntegerField( 
                help_text=_("Length (in seconds) of the media file"),
                required=False)
    
    def __init__(self, *args, **kwargs):
        super(UploadMediaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('oppia_av_upload')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'media_file',
                'media_image',
                'course_shortname',
                'length',
                Div(
                   Submit('submit', _(u'Upload'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )  
    
    def clean(self):
        cleaned_data = super(UploadMediaForm, self).clean()
        media_file = cleaned_data.get("media_file")
        media_image = cleaned_data.get("media_image")
        
        if media_file is not None:
            if media_file.content_type not in settings.OPPIA_MEDIA_FILE_TYPES:
                raise forms.ValidationError(_("You may only upload a media file which is one of the following types: %s" % ', '.join(settings.OPPIA_MEDIA_FILE_TYPES)))
        
        if media_image is not None:
            if media_image.content_type not in settings.OPPIA_MEDIA_IMAGE_FILE_TYPES:
                raise forms.ValidationError(_("You may only upload an image file which is one of the following types: %s" % ', '.join(settings.OPPIA_MEDIA_IMAGE_FILE_TYPES)))
        
        return cleaned_data