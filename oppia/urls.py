from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views import static
from django.views.generic import TemplateView
from oppia import views

# Custom HTTP response pages
handler403 = 'oppia.permissions.oppia_403_handler'

app_name = 'oppia'
urlpatterns = [

    path('', views.home_view, name="index"),
    path('server/', views.server_view, name="server"),
    path('about/', views.about_view, name="about"),
    path('teacher', views.teacher_home_view, name="teacher_index"),
    path('manager', views.manager_home_view, name="manager_index"),
    path('leaderboard', views.leaderboard_view, name="leaderboard"),

    path('upload', views.upload_step1, name="upload"),
    path('upload2/<int:course_id>', views.upload_step2, name="upload_step2"),
    path('upload2/success',
         TemplateView.as_view(template_name="course/upload-success.html"),
         name="upload_success"),

    path('course/', views.CourseListView.as_view(), name="course"),
    path('course/tag/<int:tag_id>',
         views.CourseListView.as_view(),
         name="tag_courses"),
    path('course/<int:course_id>/',
         views.CourseActivityDetail.as_view(),
         name="recent_activity"),
    path('course/<int:course_id>/edit/',
         views.upload_step2,
         {'editing': True},
         name="course_edit"),
    path('course/<int:course_id>/exports/',
         views.CourseDataExports.as_view(),
         name="course_data_exports"),
    path('course/<int:course_id>/detail/',
         views.CourseRecentActivityDetail.as_view(),
         name="recent_activity_detail"),
    path('course/<int:course_id>/exports/trackers/',
         views.ExportCourseTrackers.as_view(),
         name="export_course_trackers"),
    path('course/<int:course_id>/download',
         views.CourseDownload.as_view(),
         name="course_download"),
    path('course/<int:course_id>/structure/',
         views.CourseStructure.as_view(),
         name="course_structure"),

    path('cohort/', views.cohort_list_view, name="cohorts"),
    path('cohort/add/', views.cohort_add, name="cohort_add"),
    path('cohort/<int:cohort_id>/edit/',
         views.cohort_edit,
         name="cohort_edit"),
    path('cohort/<int:cohort_id>/view/',
         views.cohort_view,
         name="cohort_view"),
    path('cohort/<int:cohort_id>/<int:course_id>/view/',
         views.cohort_course_view,
         name="cohort_course_view"),
    path('cohort/<int:cohort_id>/leaderboard',
         views.cohort_leaderboard_view,
         name="cohort_leaderboard"),

    path('view/',
         views.AppLauncherDetailView.as_view(),
         name="app_launch_activity_redirect"),
    url(r'^media/(?P<path>.*)$',
        static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]
