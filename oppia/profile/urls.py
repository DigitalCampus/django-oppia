# oppia/profile/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^register/$', 'oppia.profile.views.register', name="profile_register"),
    url(r'^register/thanks/$', TemplateView.as_view(template_name="oppia/thanks.html"), name="profile_register_thanks"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'oppia/login.html',}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'oppia/logout.html',}),
    url(r'^setlang/$', 'django.views.i18n.set_language', name="profile_set_language"),
    url(r'^reset/$', 'oppia.profile.views.reset', name="profile_reset"),
    url(r'^reset/sent/$', TemplateView.as_view(template_name="oppia/profile/reset-sent.html"), name="profile_reset_sent"),
    url(r'^edit/$', 'oppia.profile.views.edit', name="profile_edit"),
    url(r'^points/$', 'oppia.profile.views.points', name="profile_points"),
    url(r'^badges/$', 'oppia.profile.views.badges', name="profile_badges"),
)
