# integrations/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(staff_member_required, name='dispatch')
class HomeView(TemplateView):

    def get(self, request):
        return render(request, 'integrations/index.html')
