
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from settings import constants
from settings.models import SettingProperties


def menu_reports(request):
    # add in here any reports that need to appear

    reports = [{'name': _(u'User Registrations'),
                'description': _(u'Number of user registrations'),
                'url': reverse('reports:user_registrations'),
                'icon': 'timeline'},
               {'name': _(u'Course downloads'),
                'description': _(u'Number of course downloads'),
                'url': reverse('reports:course_downloads'),
                'icon': 'timeline'},
               {'name': _(u'Course activity'),
                'description': _(u'Course activity'),
                'url': reverse('reports:course_activity'),
                'icon': 'timeline'},
               {'name': _(u'Completion Rates'),
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
                'icon': 'timeline'},
               {'name': _(u'Monthly Active users'),
                'description': _(u'Number of unique monthly users'),
                'url': reverse('reports:maus'),
                'icon': 'timeline'},
               {'name': _(u'Total time spent'),
                'description': _(u'Total time spent on activities'),
                'url': reverse('reports:totaltimespent'),
                'icon': 'timeline'},
               {'name': _(u'Average time spent'),
                'description': _(u'Average time spent by each user'),
                'url': reverse('reports:averagetimespent'),
                'icon': 'timeline'},
               {'name': _(u'Searches'),
                'description': _(u'In-app searches'),
                'url': reverse('reports:searches'),
                'icon': 'timeline'},
               {'name': _(u'Search terms'),
                'description': _(u'Search terms used'),
                'url': reverse('reports:search_terms'),
                'icon': 'vertical_split'},
               {'name': _(u'Activity by Language'),
                'description': _(u'Activity by language'),
                'url': reverse('reports:lang_activity'),
                'icon': 'pie_chart'}]

    map_viz_enabled = SettingProperties.get_bool(
        constants.OPPIA_MAP_VISUALISATION_ENABLED,
        False)

    if map_viz_enabled:
        reports.append({'name': _(u'Activity Map'),
                        'description': _(u'Map of users locations'),
                        'url': reverse('reports:map'),
                        'icon': 'map'})
        reports.append({'name': _(u'Countries'),
                        'description': _(
                            u'Countries users are accessing from'),
                        'url': reverse('reports:countries'),
                        'icon': 'pie_chart'})

    return reports
