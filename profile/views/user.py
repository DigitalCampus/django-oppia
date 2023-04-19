from io import StringIO
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView, FormView, TemplateView, DetailView
from tastypie.models import ApiKey

from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from helpers.mixins.TitleViewMixin import TitleViewMixin
from oppia.mixins.PermissionMixins import CanEditUserMixin
from oppia.models import Points, Award, Tracker, Course, CertificateTemplate
from profile.forms import LoginForm, \
    RegisterForm, \
    ProfileForm, \
    RegenerateCertificatesForm
from profile.models import UserProfile, \
    CustomField, \
    UserProfileCustomField
from profile.utils import filter_redirect
from quiz.models import QuizAttempt, QuizAttemptResponse
from settings import constants
from settings.models import SettingProperties

STR_COMMON_FORM = 'common/form/form.html'
STR_OPPIA_HOME = 'oppia:index'


class LoginView(TitleViewMixin, FormView):
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


class RegisterView(TitleViewMixin, FormView):

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
        form.save()
        # Create new user
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        u = authenticate(username=username, password=password)
        if u is not None and u.is_active:
            login(self.request, u)

        return super().form_valid(form)


class EditView(CanEditUserMixin, UpdateView):

    model = User
    form_class = ProfileForm
    context_object_name = 'view_user'
    template_name = 'profile/profile.html'
    pk_url_kwarg = 'user_id'

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.allow_edit = SettingProperties \
            .get_bool(constants.OPPIA_ALLOW_PROFILE_EDITING,
                      settings.OPPIA_ALLOW_PROFILE_EDITING)

    def get_object(self, queryset=None):
        if self.pk_url_kwarg in self.kwargs:
            return super().get_object()
        else:
            return self.request.user

    def get_success_url(self):
        # We return after success to the same view
        return self.request.path

    def get_form_kwargs(self):
        """As it is not a ModelForm, we remove the instance argument"""
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance')
        kwargs.update({'allow_edit': self.allow_profile_editing()})
        return kwargs

    def get_initial(self):
        key = ApiKey.objects.get(user=self.object)
        user_profile, created = UserProfile.objects \
            .get_or_create(user=self.object)

        initial = {
            'username': self.object.username,
            'email': self.object.email,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'api_key': key.key,
            'job_title': user_profile.job_title,
            'organisation': user_profile.organisation,
            'phone_number': user_profile.phone_number,
            'exclude_from_reporting': user_profile.exclude_from_reporting
        }

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            upcf_row = UserProfileCustomField.objects \
                .filter(key_name=custom_field, user=self.object)
            if upcf_row.exists():
                initial[custom_field.id] = upcf_row.first().get_value()

        return initial

    def form_valid(self, form):
        if self.allow_profile_editing():
            self.edit_form_process(form, self.object)
            messages.success(self.request, _(u"Profile updated"))

        # if password should be changed
        password = form.cleaned_data.get("password", )
        if password:
            self.object.set_password(password)
            self.object.save()
            messages.success(self.request, _(u"Password updated"))

        return self.render_to_response(self.get_context_data(form=form))

    def allow_profile_editing(self):
        return self.allow_edit or self.request.user.is_staff

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
        user_profile.job_title = form.cleaned_data.get('job_title')
        user_profile.organisation = form.cleaned_data.get('organisation')
        user_profile.phone_number = form.cleaned_data.get('phone_number')

        if self.request.user.is_staff:
            user_profile.exclude_from_reporting = form.cleaned_data.get('exclude_from_reporting')
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


class RegenerateCertificatesView(CanEditUserMixin, DetailView, FormView):
    model = User
    form_class = RegenerateCertificatesForm
    context_object_name = 'user'
    template_name = 'profile/certificates/regenerate.html'
    pk_url_kwarg = 'user_id'
    success_url = 'success/'

    def get_initial(self):
        user = self.get_object()
        return {
            'email': user.email,
            'old_email': user.email
        }

    def get_object(self, queryset=None):
        if self.pk_url_kwarg in self.kwargs:
            return super().get_object()
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        awards = Award.objects.filter(user=self.object)
        certificates = []
        for award in awards:
            try:
                course = Course.objects.get(awardcourse__award=award)
            except Course.DoesNotExist:
                continue
            badge = award.badge
            certs = CertificateTemplate.objects.filter(course=course, badge=badge, enabled=True)
            for cert in certs:
                certificate = {}
                certificate['course'] = course
                certificate['badge'] = badge
                valid, display_name = cert.display_name(self.object)
                certificate['display_name'] = display_name
                certificate['cert_link'] = award.certificate_pdf
                certificates.append(certificate)

        context['user'] = self.object
        context['certificates'] = certificates
        return context

    def form_valid(self, form):
        user = self.get_object()
        old_email = form.cleaned_data.get("old_email")
        new_email = form.cleaned_data.get("email")
        if old_email != new_email:
            user.email = new_email
            user.save()

        user_command = "--user=" + str(user.id)
        call_command('generate_certificates', user_command, stdout=StringIO())
        return super().form_valid(form)
