
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def menu_reports(request):
    # add in here any reports that need to appear in the menu
    # return [{'name': 'test',
    #            'url':'/reports/1/'},
    #         {'name': 'test2',
    #            'url':'/reports/2/'}]
    return [{'name': _('Completion Rates'),
             'url': reverse('reports:completion_rates')},
            {'name': _('Unique Users'),
             'url': reverse('reports:unique_users')}]
