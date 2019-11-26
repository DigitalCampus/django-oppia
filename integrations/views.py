# integrations/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def home(request):
    return render(request, 'integrations/index.html')
