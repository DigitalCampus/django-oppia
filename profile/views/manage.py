import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from tastypie.models import ApiKey

import profile
from oppia.models import Points, Award, Tracker
from profile.forms import UploadProfileForm, \
    UserSearchForm, \
    DeleteAccountForm
from profile.models import UserProfile
from profile.views.utils import get_paginated_users, \
                                get_filters_from_row, \
                                get_query
from quiz.models import QuizAttempt, QuizAttemptResponse


@staff_member_required
def search_users(request):
    users = User.objects

    filtered = False
    search_form = UserSearchForm(request.GET, request.FILES)
    if search_form.is_valid():
        filters = get_filters_from_row(search_form)
        if filters:
            users = users.filter(**filters)
            filtered = True

    if not filtered:
        users = users.all()

    query_string = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        filter_query = get_query(query_string, ['username',
                                                'first_name',
                                                'last_name',
                                                'email', ])
        users = users.filter(filter_query)

    ordering = request.GET.get('order_by', None)
    if ordering is None:
        ordering = 'first_name'

    users = users.order_by(ordering)
    paginator = Paginator(users, profile.SEARCH_USERS_RESULTS_PER_PAGE)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)

    return render(request, 'profile/search_user.html',
                  {'quicksearch': query_string,
                   'search_form': search_form,
                   'advanced_search': filtered,
                   'page': users,
                   'page_ordering': ordering})


@staff_member_required
def export_users(request):

    ordering, users = get_paginated_users(request)
    for user in users:
        try:
            user.apiKey = user.api_key.key
        except ApiKey.DoesNotExist:
            # if the user doesn't have an apiKey yet, generate it
            user.apiKey = ApiKey.objects.create(user=user).key

    template = 'export-users.html'
    if request.is_ajax():
        template = 'users-paginated-list.html'

    return render(request, 'profile/' + template,
                  {'page': users,
                   'page_ordering': ordering,
                   'users_list_template': 'export'})


@staff_member_required
def list_users(request):
    ordering, users = get_paginated_users(request)
    return render(request, 'profile/users-paginated-list.html',
                  {'page': users,
                   'page_ordering': ordering,
                   'users_list_template': 'select',
                   'ajax_url': request.path})


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

            # delete points
            Points.objects.filter(user=delete_user).delete()

            # delete badges
            Award.objects.filter(user=delete_user).delete()

            # delete trackers
            Tracker.objects.filter(user=delete_user).delete()

            # delete quiz attempts
            QuizAttemptResponse.objects \
                .filter(quizattempt__user=delete_user).delete()
            QuizAttempt.objects.filter(user=delete_user).delete()

            # delete profile
            UserProfile.objects.filter(user=delete_user).delete()

            # delete api key
            ApiKey.objects.filter(user=delete_user).delete()

            # logout and delete user
            User.objects.get(pk=delete_user.id).delete()

            # redirect
            return HttpResponseRedirect(
                reverse('profile:delete_complete'))
    else:
        form = DeleteAccountForm(initial={'username': request.user.username})

    return render(request, 'profile/delete_account.html',
                  {'form': form})


def delete_account_complete_view(request):

    return render(request, 'profile/delete_account_complete.html')


class UploadUsers(View):

    form_class = UploadProfileForm
    template_name = 'profile/upload.html'

    def get(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

        results = []
        form = self.form_class()

        return render(request, self.template_name,
                      {'form': form,
                       'results': results})

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

        results = []
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            csv_file = csv.DictReader(
                chunk.decode() for chunk in request.FILES['upload_file'])
            required_fields = ['username', 'firstname', 'lastname', 'email']
            results = self.process_upload_user_file(csv_file, required_fields)

        return render(request, self.template_name,
                      {'form': form,
                       'results': results})

    def process_upload_user_file(self, csv_file, required_fields):
        results = []
        try:
            for row in csv_file:
                # check all required fields defined
                all_defined = True
                for rf in required_fields:
                    if rf not in row or row[rf].strip() == '':
                        result = {}
                        result['username'] = row['username']
                        result['created'] = False
                        result['message'] = _(u'No %s set' % rf)
                        results.append(result)
                        all_defined = False

                if not all_defined:
                    continue

                results.append(self.process_upload_file_save_user(row))

        except Exception:
            result = {}
            result['username'] = None
            result['created'] = False
            result['message'] = _(u'Could not parse file')
            results.append(result)

        return results

    def process_upload_file_save_user(self, row):
        user = User()
        user.username = row['username']
        user.first_name = row['firstname']
        user.last_name = row['lastname']
        user.email = row['email']
        auto_password = False
        if 'password' in row:
            user.set_password(row['password'])
        else:
            password = User.objects.make_random_password()
            user.set_password(password)
            auto_password = True
        try:
            user.save()
        except IntegrityError:
            result = {}
            result['username'] = row['username']
            result['created'] = False
            result['message'] = _(u'User already exists')
            return result

        up = UserProfile()
        up.user = user
        for col_name in row:
            setattr(up, col_name, row[col_name])
        up.save()
        result = {}
        result['username'] = row['username']
        result['created'] = True
        if auto_password:
            result['message'] = \
                _(u'User created with password: %s' % password)
        else:
            result['message'] = _(u'User created')

        return result
