from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div

from django import forms
from django.utils.translation import ugettext_lazy as _


class EditCoursePointsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)

        super(EditCoursePointsForm, self).__init__(* args, ** kwargs)
        for event in initial:
            try:
                self.fields[event.event] = \
                    forms.IntegerField(initial=event.points,
                                       label=event.label,
                                       help_text=event.helper_text)
            except AttributeError:
                self.fields[event.event] = \
                    forms.IntegerField(initial=event.points,
                                       label=event.get_label(),
                                       help_text=event.get_helper_text())

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout()

        for object in initial:
            self.helper.layout.append(object.event)

        self.helper.layout.append(
                Div(
                   Submit('submit',
                          _(u'Update points'),
                          css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ))

    def clean(self):
        cleaned_data = super(EditCoursePointsForm, self).clean()
        return cleaned_data


class EditActivityPointsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)

        super(EditActivityPointsForm, self).__init__(* args, ** kwargs)
        for event in initial:
            try:
                self.fields[event.event] = \
                    forms.IntegerField(initial=int(event.points),
                                       label=event.get_label(),
                                       help_text=event.get_helper_text())
            except AttributeError:
                self.fields[event.event.event] = \
                    forms.IntegerField(initial=int(event.points),
                                       label=event.get_label(),
                                       help_text=event.get_helper_text())

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-18'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout()

        for event in initial:
            try:
                self.helper.layout.append(event.event)
            except AttributeError:
                self.helper.layout.append(event['event'])

        self.helper.layout.append(
                Div(
                   Submit('submit',
                          _(u'Update points'),
                          css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ))

    def clean(self):
        cleaned_data = super(EditActivityPointsForm, self).clean()
        return cleaned_data


class EditMediaPointsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)

        super(EditMediaPointsForm, self).__init__(* args, ** kwargs)
        for event in initial:
            try:
                self.fields[event.event] = \
                    forms.IntegerField(initial=int(event.points),
                                       label=event.get_label(),
                                       help_text=event.get_helper_text())
            except AttributeError:
                self.fields[event.event.event] = \
                    forms.IntegerField(initial=int(event.points),
                                       label=event.get_label(),
                                       help_text=event.get_helper_text())

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-18'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout()

        for event in initial:
            try:
                self.helper.layout.append(event.event)
            except AttributeError:
                self.helper.layout.append(event['event'])

        self.helper.layout.append(
                Div(
                   Submit('submit',
                          _(u'Update points'),
                          css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ))

    def clean(self):
        cleaned_data = super(EditMediaPointsForm, self).clean()
        return cleaned_data


class GamificationEventForm(forms.Form):
    level = forms.CharField(widget=forms.HiddenInput())
    event = forms.CharField(widget=forms.HiddenInput())
    points = forms.IntegerField(widget=forms.HiddenInput())
    reference = forms.IntegerField(widget=forms.HiddenInput())
