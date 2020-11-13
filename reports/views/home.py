
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from reports.signals import dashboard_accessed


@method_decorator(staff_member_required, name='dispatch')
class HomeView(TemplateView):

    def get(self, request):
        dashboard_accessed.send(sender=None, request=request, data=None)
        return render(request, 'reports/home.html')
