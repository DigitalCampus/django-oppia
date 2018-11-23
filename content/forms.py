# oppia/content/forms.py

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Row


class MediaEmbedHelperForm(forms.Form):
    media_url = forms.CharField(
                help_text=_("The url to your media - this should be a url to download the actual media file (.avi, .m4v/.mp4 or .mp3) , NOT a link to media streaming service such as YouTube, Vimeo etc"),
                required=True,
                error_messages={'required': _('Please enter the media url')}, )

    def __init__(self, *args, **kwargs):
        super(MediaEmbedHelperForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'media_url',
                Div(
                   Submit('submit', _(u'Go'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )

    def clean(self):
        cleaned_data = super(MediaEmbedHelperForm, self).clean()

        return cleaned_data
