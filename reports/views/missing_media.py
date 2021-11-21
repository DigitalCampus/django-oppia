

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from oppia.models import Tracker


@method_decorator(staff_member_required, name='dispatch')
class MissingMediaView(TemplateView):
    
    def get(self, request):
        users = Tracker.objects.filter(event="media_missing")
        
        
        return render(request, 'reports/missing_media.html',
                      )