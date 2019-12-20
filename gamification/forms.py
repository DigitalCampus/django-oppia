
from django import forms


class GamificationEventForm(forms.Form):
    level = forms.CharField(widget=forms.HiddenInput())
    event = forms.CharField(widget=forms.HiddenInput())
    points = forms.IntegerField(widget=forms.HiddenInput())
    reference = forms.IntegerField(widget=forms.HiddenInput())
