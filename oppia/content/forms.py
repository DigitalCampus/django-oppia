# oppia/content/forms.py

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Row


class VideoEmbedHelperForm(forms.Form):
    video_url = forms.CharField(
                help_text=_("The url to your video - this should be a url to download the actual video file (.avi, .m4v or .mp4) , NOT a link to video streaming service such as YouTube, Vimeo etc"),
                required=True,
                error_messages={'required': _('Please enter the video url')},)
    
    def __init__(self, *args, **kwargs):
        super(VideoEmbedHelperForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'video_url',
                Div(
                   Submit('submit', _(u'Go'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )  
    
    def clean(self):
        cleaned_data = super(VideoEmbedHelperForm, self).clean()
        
        return cleaned_data