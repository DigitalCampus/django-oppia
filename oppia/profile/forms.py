from django import forms
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, 
                               min_length=4,
                               error_messages={'required': _(u'Please enter a username.')},)
    email = forms.CharField(validators=[validate_email],
                                error_messages={'invalid': _(u'Please enter a valid e-mail address.'),
                                                'required': _(u'Please enter your e-mail address.')},
                                required=True)
    password = forms.CharField(widget=forms.PasswordInput,
                                error_messages={'required': _(u'Please enter a password.'),
                                                'min_length': _(u'Your password should be at least 6 characters long.')},
                                min_length=6,       
                                required=True)
    password_again = forms.CharField(widget=forms.PasswordInput,
                                    min_length=6,
                                    error_messages={'required': _(u'Please enter your password again.'),
                                                    'min_length': _(u'Your password again should be at least 6 characters long.')},
                                    required=True)
    first_name = forms.CharField(max_length=100,
                                    error_messages={'required': _(u'Please enter your first name.'),
                                                    'min_length': _(u'Your first name should be at least 2 characters long.')},
                                    min_length=2,
                                    required=True)
    last_name = forms.CharField(max_length=100,
                                error_messages={'required': _(u'Please enter your last name.'),
                                                'min_length': _(u'Your last name should be at least 2 characters long.')},
                                min_length=2,
                                required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        username = cleaned_data.get("username")

        # check the username not already used
        num_rows = User.objects.filter(username=username).count()
        if num_rows != 0:
            raise forms.ValidationError( _(u"Username has already been registered, please select another."))
        
        # check the email address not already used
        num_rows = User.objects.filter(email=email).count()
        if num_rows != 0:
            raise forms.ValidationError( _(u"Email has already been registered"))

        # check the password are the same
        if password and password_again:
            if password != password_again:
                raise forms.ValidationError( _(u"Passwords do not match."))

        # Always return the full collection of cleaned data.
        return cleaned_data

class ResetForm(forms.Form):
    username = forms.CharField(max_length=30,
        error_messages={'invalid': _(u'Please enter a username.')},
        required=True)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        num_rows = User.objects.filter(username__exact=username).count()
        if num_rows != 1:
            raise forms.ValidationError( _(u"Username not found"))
        return cleaned_data

class ProfileForm(forms.Form):
    api_key = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}),
                               required=False)
    username = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}),
                               required=False)
    email = forms.CharField(validators=[validate_email],
                            error_messages={'invalid': _(u'Please enter a valid e-mail address.')},
                            required=True)
    password = forms.CharField(widget=forms.PasswordInput,
                               required=False,
                               min_length=6,
                               error_messages={'min_length': _(u'Your new password should be at least 6 characters long')},)
    password_again = forms.CharField(widget=forms.PasswordInput,
                                     required=False,
                                     min_length=6)
    first_name = forms.CharField(max_length=100,
                                 min_length=2,
                                 required=True)
    last_name = forms.CharField(max_length=100,
                                min_length=2,
                                required=True)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProfileForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        # check email not used by anyone else
        email = cleaned_data.get("email")
        num_rows = User.objects.exclude(username__exact=self.request.user.username).filter(email=email).count()
        if num_rows != 0:
            raise forms.ValidationError( _(u"Email address already in use"))
        
        # if password entered then check they are the same
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        if password and password_again:
            if password != password_again:
                raise forms.ValidationError( _(u"Passwords do not match."))
            
        return cleaned_data