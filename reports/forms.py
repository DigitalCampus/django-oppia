
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit

from django import forms
from django.utils.translation import ugettext_lazy as _

from profile.models import CustomField


class ReportGroupByForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ReportGroupByForm, self).__init__(* args, ** kwargs)

        # this need to be defined here, rather than as a class attribute,
        # otherwise the tests fail (presume due to class loading ordering?)
        self.fields['group_by'] = forms.ChoiceField(
            choices=[(cf.id, cf.label) for cf in CustomField.objects.all()],
            label=_('Group by'),
            widget=forms.Select,
            required=False,
        )

        self.helper = FormHelper()
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'group_by',
                Div(
                   Submit('submit',
                          _(u'Filter'),
                          css_class='btn btn-default')
                ),
            )

    def clean(self):
        cleaned_data = super(ReportGroupByForm, self).clean()
        return cleaned_data
