

def integrations(request):
    return render(request, 'oppia/integrations/dhis2/index.html',
                              {'settings': settings},
                              content_type="application/json")