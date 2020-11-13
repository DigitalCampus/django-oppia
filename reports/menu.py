
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
             'icon': 'vertical_split'},
            {'name': _(u'Daily Active users'),
             'description': _(u'Number of unique daily users'),
             'url': reverse('reports:daus'),
             'icon': 'vertical_split'},
            {'name': _(u'Monthly Active users'),
             'description': _(u'Number of unique monthly users'),
             'url': reverse('reports:maus'),
             'icon': 'vertical_split'},
            {'name': _(u'Total time spent'),
             'description': _(u'Total time spent on activities'),
             'url': reverse('reports:totaltimespent'),
             'icon': 'vertical_split'},
            {'name': _(u'Average time spent'),
             'description': _(u'Average time spent by each user'),
             'url': reverse('reports:averagetimespent'),
             'icon': 'vertical_split'}]
