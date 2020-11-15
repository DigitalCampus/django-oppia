
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from profile.models import UserProfileCustomField

from reports.forms import ReportGroupByForm
from reports.signals import dashboard_accessed


@method_decorator(staff_member_required, name='dispatch')
class UniqueUsersView(TemplateView):

    def get(self, request):
        dashboard_accessed.send(sender=None, request=request, data=None)
        user_count = User.objects.all().count()
        group_by_form = ReportGroupByForm()
        return render(request, 'reports/unique_users.html',
                      {'user_count': user_count,
                       'form': group_by_form})

    def post(self, request):
        dashboard_accessed.send(sender=None, request=request, data=None)
        user_list = []
        group_by_form = ReportGroupByForm(request.POST)
        if group_by_form.is_valid():
            group_by = group_by_form.cleaned_data.get("group_by")
            user_list = UserProfileCustomField.objects \
                .filter(key_name=group_by) \
                .values('value_str') \
                .annotate(total=Count('value_str')) \
                .order_by('value_str')
        return render(request, 'reports/unique_users.html',
                      {'user_list': user_list,
                       'form': group_by_form,
                       'filter': group_by})
