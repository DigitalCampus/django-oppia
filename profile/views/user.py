from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView, FormView, TemplateView

from io import StringIO

from tastypie.models import ApiKey

from urllib.parse import urlparse

from helpers.mixins.TitleViewMixin import TitleViewMixin
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from oppia.models import Points, Award, Tracker, Course, CertificateTemplate
from oppia.permissions import can_edit_user
from profile.forms import LoginForm, \
                          RegisterForm, \
                          ProfileForm, \
                          RegenerateCertificatesForm

from profile.models import UserProfile, \
                           CustomField, \
                           UserProfileCustomField

from profile.views.utils import filter_redirect

from quiz.models import QuizAttempt, QuizAttemptResponse

from settings import constants
from settings.models import SettingProperties

STR_COMMON_FORM = 'common/form/form.html'
STR_OPPIA_HOME = 'oppia:index'


class LoginView(FormView, TitleViewMixin):
    template_name = STR_COMMON_FORM
    form_class = LoginForm
    title = _(u'Login')

    def get_initial(self):
        return {'next': filter_redirect(self.request.GET)}

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse(STR_OPPIA_HOME))
        return super().dispatch(*args, **kwargs)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        next_page = filter_redirect(self.request.POST)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            if next_page is not None:
                parsed_uri = urlparse(next_page)
                if parsed_uri.netloc == '':
                    return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(reverse(STR_OPPIA_HOME))


class RegisterView(FormView, TitleViewMixin):

    template_name = STR_COMMON_FORM
    form_class = RegisterForm
    success_url = 'thanks/'
    title = _(u'Register')

    def dispatch(self, *args, **kwargs):
        self_register = SettingProperties.get_bool(
            constants.OPPIA_ALLOW_SELF_REGISTRATION,
            settings.OPPIA_ALLOW_SELF_REGISTRATION)
        if not self_register:
            raise Http404
        else:
            return super().dispatch(*args, **kwargs)

    def get_initial(self):
        return {'next': filter_redirect(self.request.GET)}

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create new user
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        self.register_form_process(form)

        u = authenticate(username=username, password=password)
        if u is not None and u.is_active:
            login(self.request, u)

        return response

    def register_form_process(self, form):
        # Create new user
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # create UserProfile record
        UserProfile.objects.create(
            user=user,
            job_title=form.cleaned_data.get("job_title"),
            organisation=form.cleaned_data.get("organisation")
        )

        # save any custom fields
        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            if custom_field.type == 'int':
                profile_field = UserProfileCustomField(
                    key_name=custom_field,
                    user=user,
                    value_int=form.cleaned_data.get(custom_field.id))
            elif custom_field.type == 'bool':
                profile_field = UserProfileCustomField(
                    key_name=custom_field,
                    user=user,
                    value_bool=form.cleaned_data.get(custom_field.id))
            else:
                profile_field = UserProfileCustomField(
                    key_name=custom_field,
                    user=user,
                    value_str=form.cleaned_data.get(custom_field.id))

            if (form.cleaned_data.get(custom_field.id) is not None
                and form.cleaned_data.get(custom_field.id) != '') \
                    or custom_field.required is True:
                profile_field.save()


class EditView(UpdateView):

    model = User
    form_class = ProfileForm
    context_object_name = 'user'
    template_name = 'profile/profile.html'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id', )
        if user_id:
            if can_edit_user(self.request, user_id):
                return User.objects.get(pk=user_id)
            else:
                raise PermissionDenied
        else:
            return self.request.user

    def get_success_url(self):
        # We return after success to the same view
        return self.request.path

    def get_form_kwargs(self):
        """As it is not a ModelForm, we remove the instance argument"""
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance')
        return kwargs

    def get_initial(self):
        key = ApiKey.objects.get(user=self.object)
        user_profile, created = UserProfile.objects \
            .get_or_create(user=self.object)

        initial = {'username': self.object.username,
                   'email': self.object.email,
                   'first_name': self.object.first_name,
                   'last_name': self.object.last_name,
                   'api_key': key.key,
                   'job_title': user_profile.job_title,
                   'organisation': user_profile.organisation}

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            upcf_row = UserProfileCustomField.objects \
                .filter(key_name=custom_field, user=self.object)
            if upcf_row.exists():
                initial[custom_field.id] = upcf_row.first().get_value()

        return initial

    def form_valid(self, form):
        self.edit_form_process(form, self.object)
        messages.success(self.request, _(u"Profile updated"))

        # if password should be changed
        password = form.cleaned_data.get("password", )
        if password:
            self.object.set_password(password)
            self.object.save()
            messages.success(self.request, _(u"Password updated"))

        return self.render_to_response(self.get_context_data(form=form))

    def edit_form_process(self, form, view_user):
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        view_user.email = email
        view_user.first_name = first_name
        view_user.last_name = last_name
        view_user.save()

        user_profile, created = UserProfile.objects \
            .get_or_create(user=view_user)
        user_profile.job_title = form.cleaned_data.get("job_title")
        user_profile.organisation = form.cleaned_data.get("organisation")
        user_profile.save()

        # save any custom fields
        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            if (form.cleaned_data.get(custom_field.id) is not None
                and form.cleaned_data.get(custom_field.id) != '') \
                    or custom_field.required is True:

                profile_field, created = UserProfileCustomField.objects \
                    .get_or_create(key_name=custom_field, user=view_user)

                if custom_field.type == 'int':
                    profile_field.value_int = \
                        form.cleaned_data.get(custom_field.id)
                elif custom_field.type == 'bool':
                    profile_field.value_bool = \
                        form.cleaned_data.get(custom_field.id)
                else:
                    profile_field.value_str = \
                        form.cleaned_data.get(custom_field.id)

                profile_field.save()


class ExportDataView(TemplateView):

    def get(self, request, data_type):
        if data_type == 'activity':
            my_activity = Tracker.objects.filter(user=request.user)
            return render(request, 'profile/export/activity.html',
                          {'activity': my_activity})
        elif data_type == 'quiz':
            my_quizzes = []
            my_quiz_attempts = QuizAttempt.objects.filter(user=request.user)
            for mqa in my_quiz_attempts:
                data = {}
                data['quizattempt'] = mqa
                data['quizattemptresponses'] = QuizAttemptResponse.objects \
                    .filter(quizattempt=mqa)
                my_quizzes.append(data)

            return render(request, 'profile/export/quiz_attempts.html',
                          {'quiz_attempts': my_quizzes})
        elif data_type == 'points':
            points = Points.objects.filter(user=request.user)
            return render(request, 'profile/export/points.html',
                          {'points': points})
        elif data_type == 'badges':
            badges = Award.objects.filter(user=request.user)
            return render(request, 'profile/export/badges.html',
                          {'badges': badges})
        elif data_type == 'profile':
            profile, additional_profile, custom_profile =  \
                self.get_profile_data(request.user)
            return render(request, 'profile/export/profile.html',
                          {'profile': profile,
                           'additional_profile': additional_profile,
                           'custom_profile': custom_profile})
        else:
            raise Http404

    @staticmethod
    def get_profile_data(user):
        profile = User.objects.get(pk=user.id)
        additional_profile = UserProfile.objects.get(user=user)
        custom_profile_fields = CustomField.objects.filter(
            userprofilecustomfield__user=user).order_by('order')
        custom_profile = []
        for cpf in custom_profile_fields:
            cp = {}
            cp['label'] = cpf.label
            cp['value'] = UserProfileCustomField.objects.get(
                key_name=cpf.id, user=user).get_value()
            custom_profile.append(cp)
        return profile, additional_profile, custom_profile


class PointsView(SafePaginatorMixin, ListView):
    template_name = 'profile/points.html'
    paginate_by = 25

    def get_queryset(self):
        return Points.objects.filter(user=self.request.user).order_by('-date')


class BadgesView(ListView):
    context_object_name = 'awards'
    template_name = 'profile/badges.html'

    def get_queryset(self):
        return Award.objects.filter(
            user=self.request.user).order_by('-award_date')


class RegenerateCertificatesView(TemplateView):

    def get(self, request, user_id=None):
        if user_id:
            if can_edit_user(request, user_id):
                user = User.objects.get(pk=user_id)
            else:
                raise PermissionDenied
        else:
            user = request.user
  
        initial = {'email': user.email,
                   'old_email': user.email }
        form = RegenerateCertificatesForm(initial=initial)
        awards = Award.objects.filter(user=user)
        certificates = []
        for award in awards:
            course = Course.objects.get(awardcourse__award=award)
            badge = award.badge
            certs = CertificateTemplate.objects.filter(course=course,
                                                       badge=badge,
                                                       enabled=True)
            
            for cert in certs:
                certificate = {}
                certificate['course'] = course
                certificate['badge'] = badge
                valid, display_name = cert.display_name(user)
                certificate['display_name'] = display_name
                certificates.append(certificate)
                
        return render(request, 'profile/certificates/regenerate.html',
                          {'user': user,
                           'form': form,
                           'certificates': certificates})
        
    def post(self, request, user_id=None):
        if user_id:
            if can_edit_user(request, user_id):
                user = User.objects.get(pk=user_id)
            else:
                raise PermissionDenied
        else:
            user = request.user
            
        # update email address if changed
        old_email = request.POST.get("old_email")
        new_email = request.POST.get("email")
        if old_email != new_email:
            user.email = new_email
            user.save()
            
        user_command = "--user=" + str(user.id)
        call_command('generate_certificates', user_command, stdout=StringIO())
        
        return HttpResponseRedirect('success/')
