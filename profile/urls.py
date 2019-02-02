# oppia/profile/urls.py
from django.conf.urls import url
from django.contrib.auth import views as django_contrib_auth_views
from django.views import i18n as django_views_i18n
from django.views.generic import TemplateView

from profile import views as oppia_profile_views

urlpatterns = [
    url(r'^register/$', oppia_profile_views.register, name="profile_register"),
    url(r'^register/thanks/$', TemplateView.as_view(template_name="oppia/thanks.html"), name="profile_register_thanks"),
    url(r'^login/$', oppia_profile_views.login_view, name="profile_login"),
    url(r'^logout/$', django_contrib_auth_views.logout, {'template_name': 'oppia/logout.html', }, name="profile_logout"),
    url(r'^setlang/$', django_views_i18n.set_language, name="profile_set_language"),
    url(r'^reset/$', oppia_profile_views.reset, name="profile_reset"),
    url(r'^reset/sent/$', TemplateView.as_view(template_name="oppia/profile/reset-sent.html"), name="profile_reset_sent"),
    url(r'^edit/$', oppia_profile_views.edit, name="profile_edit"),
    url(r'^edit/(?P<user_id>\d+)/$', oppia_profile_views.edit, name="profile_edit_user"),
    url(r'^points/$', oppia_profile_views.points, name="profile_points"),
    url(r'^badges/$', oppia_profile_views.badges, name="profile_badges"),
    url(r'^(?P<user_id>\d+)/activity/$', oppia_profile_views.user_activity, name="profile_user_activity"),
    url(r'^(?P<user_id>\d+)/(?P<course_id>\d+)/activity/$', oppia_profile_views.user_course_activity_view, name="profile_user_course_activity"),
    url(r'^upload/$', oppia_profile_views.upload_view, name="profile_upload"),
    url(r'^search/$', oppia_profile_views.search_users, name="profile_search_users"),
    url(r'^export/$', oppia_profile_views.export_users, name="profile_export"),
    url(r'^list/$', oppia_profile_views.list_users, name="profile_list_users"),
    
    url(r'^delete/$', oppia_profile_views.delete_account_view, name="profile_delete_account"),
    url(r'^delete/complete/$', oppia_profile_views.delete_account_complete_view, name="profile_delete_account_complete"),
    url(r'^export/mydata/(?P<data_type>\w[\w/-]*)$', oppia_profile_views.export_mydata_view, name="profile_export_mydata"),
]
