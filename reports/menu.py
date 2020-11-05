
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def menu_reports(request):
    # add in here any reports that need to appear in the menu
    # return [{'name': 'test',
    #            'url':'/reports/1/'},
    #         {'name': 'test2',
    #            'url':'/reports/2/'}]
    return [{'name': _(u'Completion Rates'),
             'description': _(u'Completion rates for each course'),
             'url': reverse('reports:completion_rates'),
             'icon': 'vertical_split'},
            {'name': _(u'Unique Users'),
             'description': _(u'Number of unique users, grouped by \
                                registration fields'),
             'url': reverse('reports:unique_users'),
             'icon': 'vertical_split'}]
