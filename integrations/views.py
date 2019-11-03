# integrations/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


@staff_member_required
def home(request):
    return render(request, 'integrations/index.html')