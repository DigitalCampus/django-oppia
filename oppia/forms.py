from django import forms
from django.contrib.admin import widgets
from oppia.models import Schedule

class UploadCourseForm(forms.Form):
    course_file = forms.FileField()
    tags = forms.CharField(required=True)
    

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('title', 'default')
        widgets = {
            'title': forms.TextInput(attrs={'size':'60'}),     
        }
        
class ActivityScheduleForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput())
    digest =  forms.CharField(widget=forms.HiddenInput())
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    section = forms.CharField(widget=forms.HiddenInput())
    
    def clean(self):
        cleaned_data = super(ActivityScheduleForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date is None and end_date is not None:
            raise forms.ValidationError("You must enter both a start and end date.")

        if start_date is not None and end_date is None:
            raise forms.ValidationError("You must enter both a start and end date.")
        
        if start_date > end_date:
            raise forms.ValidationError("Start date must be before the end date.")

        return cleaned_data
    
class CohortForm(forms.Form):
    description = forms.CharField(required=True)
    teachers = forms.CharField(widget=forms.Textarea(), required=False)
    students = forms.CharField(widget=forms.Textarea(),required=True)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    