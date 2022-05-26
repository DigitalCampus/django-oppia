import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView, ListView
from tastypie.models import ApiKey

import profile
from helpers.mixins.PermissionMixins import AdminRequiredMixin, StaffRequiredMixin
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from helpers.mixins.TitleViewMixin import TitleViewMixin
from helpers.ajax import is_ajax
from oppia.models import Points, Award, Tracker
from profile.forms import UploadProfileForm, UserSearchForm, DeleteAccountForm, RegisterForm
from profile.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from profile.models import UserProfile, CustomField, UserProfileCustomField
from profile.views import utils, STR_COMMON_FORM
from quiz.models import QuizAttempt, QuizAttemptResponse


class UserList(StaffRequiredMixin, ExportAsCSVMixin, SafePaginatorMixin, ListView):
    model = User
    search_form = UserSearchForm
    export_filter_form = UserSearchForm
    template_name = 'profile/search_user.html'
    paginate_by = profile.SEARCH_USERS_RESULTS_PER_PAGE
    default_order = 'first_name'

    csv_filename = 'users'
    available_fields = ['username',
                        'first_name',
                        'last_name',
                        'email',
                        'userprofile__job_title',
                        'userprofile__organisation',
                        'userprofile__phone_number']

    def get_queryset(self):
        form = self.search_form(self.request.GET)
        users = User.objects

        filtered = False
        if form.is_valid():
            filters = utils.get_filters_from_row(form)
            if filters:
                users = users.filter(**filters)
                filtered = True

        if not filtered:
            users = users.all()

        users, custom_filtered = utils.get_users_filtered_by_customfields(
            users, form)
        self.filtered = filtered | custom_filtered

        query_string = self.request.GET.get('q', None)
        if query_string:
            profile_fields = ['username', 'first_name', 'last_name', 'email']
            users = users.filter(utils.get_query(query_string, profile_fields))
        ordering = self.request.GET.get('order_by', self.default_order)
        return users.distinct().order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quicksearch'] = self.request.GET.get('q', None)
        context['search_form'] = self.search_form(self.request.GET)
        context['advanced_search'] = self.filtered
        context['page_ordering'] = self.request.GET.get('order_by', self.default_order)
        return context


class AddUserView(StaffRequiredMixin, TitleViewMixin, FormView):

    template_name = STR_COMMON_FORM
    form_class = RegisterForm
    title = _('Add user')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile:users_list')


@staff_member_required
def export_users(request):

    ordering, users = utils.get_paginated_users(request)
    for user in users:
        try:
            user.apiKey = user.api_key.key
        except ApiKey.DoesNotExist:
            # if the user doesn't have an apiKey yet, generate it
            user.apiKey = ApiKey.objects.create(user=user).key

    template = 'export-users.html'
    if is_ajax(request):
        template = 'users-paginated-list.html'

    return render(request, 'profile/' + template, {
        'page_obj': users,
        'object_list': users.object_list,
        'page_ordering': ordering,
        'users_list_template': 'export' })


@staff_member_required
def list_users(request):
    ordering, users = utils.get_paginated_users(request)
    return render(request, 'profile/users-paginated-list.html',
                  {'page_obj': users,
                   'object_list': users.object_list,
                   'page_ordering': ordering,
                   'users_list_template': 'select',
                   'ajax_url': request.path})


def delete_user_data(delete_user):
    # delete points
    Points.objects.filter(user=delete_user).delete()
    # delete badges
    Award.objects.filter(user=delete_user).delete()
    # delete trackers
    Tracker.objects.filter(user=delete_user).delete()
    # delete quiz attempts
    QuizAttemptResponse.objects.filter(quizattempt__user=delete_user).delete()
    QuizAttempt.objects.filter(user=delete_user).delete()
    # delete profile
    UserProfile.objects.filter(user=delete_user).delete()
    # delete api key
    ApiKey.objects.filter(user=delete_user).delete()
    # logout and delete user
    User.objects.get(pk=delete_user.id).delete()


def delete_account_view(request, user_id):
    if request.method == 'POST':  # if form submitted...
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            posted_user = User.objects.get(pk=user_id)

            if user.is_superuser or user.id == user_id:
                delete_user = posted_user
            else:
                raise PermissionDenied

            delete_user_data(delete_user)

            # redirect
            return HttpResponseRedirect(reverse('profile:delete_complete'))
    else:
        form = DeleteAccountForm(initial={'username': request.user.username})

    return render(request, 'profile/delete_account.html',
                  {'form': form})


class DeleteAccountComplete(TemplateView):
    template_name = 'profile/delete_account_complete.html'


class UploadUsers(AdminRequiredMixin, FormView):

    form_class = UploadProfileForm
    template_name = 'profile/upload.html'

    def form_valid(self, form):
        required_fields = ['username', 'firstname', 'lastname']
        only_update = form.cleaned_data.get('only_update', False)
        csv_file = csv.DictReader(
            chunk.decode('utf-8-sig') for chunk in self.request.FILES['upload_file'])

        context = self.get_context_data(form=form)
        context['results'] = self.process_upload_user_file(csv_file,
                                                           required_fields,
                                                           only_update)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_fields"] = CustomField.objects.all().order_by('order')
        return context

    def process_upload_user_file(self, csv_file, required_fields, only_update):
        results = []
        try:
            for row in csv_file:
                # check all required fields defined
                all_defined = True
                for rf in required_fields:
                    if rf not in row or row[rf].strip() == '':
                        result = {
                            'username': row.get('username', None),
                            'created': False,
                            'message': _(u'No %s set' % rf)
                        }
                        results.append(result)
                        all_defined = False

                if not all_defined:
                    continue

                results.append(
                    self.process_upload_file_save_user(row, not only_update))

        except Exception:
            result = {
                'username': None,
                'created': False,
                'message': _(u'Could not parse file')
            }
            results.append(result)

        return results


    def process_upload_file_save_user(self, row, override_fields):
        user, user_created = User.objects.get_or_create(username=row['username'])

        password, autogenerated = self.update_user_fields(user, row, override_fields)
        self.update_user_profile(user, row, override_fields)
        self.update_custom_fields(user, row, override_fields)

        result = {
            'created': user_created,
            'username': row['username'],
        }
        if autogenerated and user_created:
            result['message'] = _(u'User created with password: %s' % password)
        elif not autogenerated and user_created:
            result['message'] = _(u'User created')
        elif autogenerated and not user_created:
            result['message'] = _(u'User updated with password: %s' % password)
        else:
            result['message'] = _(u'User updated')

        return result


    def update_user_fields(self, user, row, override_fields):
        if override_fields or not user.first_name:
            user.first_name = row['firstname']
        if override_fields or not user.last_name:
            user.last_name = row['lastname']

        if 'email' in row and (override_fields or not user.email):
            user.email = row['email']

        password = None
        auto_password = False

        # Only set password if the user doesn't have already one
        if not user.password or not user.has_usable_password():
            password = row.get('password', None)
            if not password:
                password = User.objects.make_random_password()
                auto_password = True
            user.set_password(password)

        user.save()
        return password, auto_password


    def update_user_profile(self, user, row, override_fields):
        up, created = UserProfile.objects.get_or_create(user=user)
        for col_name in row:
            if override_fields or (hasattr(up, col_name)
                                   and not getattr(up, col_name)):
                setattr(up, col_name, row[col_name])
        up.save()


    def update_custom_fields(self, user, row, override_fields):
        custom_fields = CustomField.objects.all()
        for cf in custom_fields:
            if cf.id in row:
                upcf, created = UserProfileCustomField.objects.get_or_create(
                    user=user, key_name=cf)
                if cf.type == 'bool':
                    if override_fields or upcf.value_bool is None:
                        upcf.value_bool = row[cf.id]
                elif cf.type == 'int':
                    if override_fields or not upcf.value_int:
                        upcf.value_int = row[cf.id]
                else:
                    if override_fields or not upcf.value_str:
                        upcf.value_str = row[cf.id]
                upcf.save()
