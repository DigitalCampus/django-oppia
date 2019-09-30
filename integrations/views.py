from django.shortcuts import render 
from django.utils.translation import ugettext_lazy as _

def integrations(request):
    integrations = {}
    return render(request, 'integrations/index.html',
                              {'integrations': integrations})