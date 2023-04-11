from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView
from oppia import views
from django.conf.urls.static import static

# Custom HTTP response pages
handler403 = 'oppia.permissions.oppia_403_handler'

app_name = 'oppia'
urlpatterns = [

    path('', views.HomeView.as_view(), name="index"),
    path('server/', views.ServerView.as_view(), name="server"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('teacher', views.TeacherView.as_view(), name="teacher_index"),
    path('manager', views.ManagerView.as_view(), name="manager_index"),
    path('leaderboard', views.LeaderboardView.as_view(), name="leaderboard"),

    path('upload', views.UploadStep1.as_view(), name="upload"),
    path('upload2/<int:course_id>', views.UploadStep2.as_view(), name="upload_step2"),
    path('upload2/success', TemplateView.as_view(template_name="course/upload-success.html"), name="upload_success"),

    path('course/', views.CourseListView.as_view(), name="course"),
    path('course_manage/', views.ManageCourseList.as_view(), name="course_manage"),
    path('course/category/<int:category_id>', views.CourseListView.as_view(), name="category_courses"),
    path('course/<int:course_id>/', views.CourseActivityDetail.as_view(), name="recent_activity"),
    path('course/<int:course_id>/edit/', views.EditCourse.as_view(), name="course_edit"),
    path('course/<int:course_id>/exports/', views.CourseDataExports.as_view(), name="course_data_exports"),
    path('course/<int:course_id>/detail/', views.CourseActivityDetailList.as_view(), name="recent_activity_detail"),
    path('course/<int:course_id>/exports/trackers/',
         views.ExportCourseTrackers.as_view(),
         name="export_course_trackers"),
    path('course/<int:course_id>/download',  views.CourseDownload.as_view(), name="course_download"),
    path('course/<int:course_id>/structure/', views.CourseStructure.as_view(), name="course_structure"),

    path('course/<int:course_id>/feedback/', views.CourseFeedbackActivitiesList.as_view(), name="course_feedback"),
    path('course/<int:course_id>/feedback/<int:feedback_id>/responses/',
         views.CourseFeedbackResponsesList.as_view(),
         name="course_feedback_responses"),
    path('course/<int:course_id>/feedback/<int:quiz_id>/responses/<int:pk>',
         views.FeedbackResponseDetail.as_view(),
         name="feedback_response_detail"),

    path('cohort/', views.CohortListView.as_view(), name="cohorts"),
    path('cohort/add/', views.AddCohortView.as_view(), name="cohort_add"),
    path('cohort/<int:cohort_id>/edit/', views.CohortEditView.as_view(), name="cohort_edit"),
    path('cohort/<int:cohort_id>/view/', views.CohortDetailView.as_view(), name="cohort_view"),
    path('cohort/<int:cohort_id>/<int:course_id>/view/', views.cohort_course_view, name="cohort_course_view"),
    path('cohort/<int:cohort_id>/leaderboard', views.CohortLeaderboardView.as_view(), name="cohort_leaderboard"),

    path('certificate/preview/<int:certificate_template_id>/',
         views.PreviewCertificateView.as_view(),
         name="certificate_preview"),
    path('certificate/validate/<str:validation_uuid>/',
         views.ValidateCertificateView.as_view(),
         name="certificate_validate"),

    path('view/',
         views.AppLauncherDetailView.as_view(),
         name="app_launch_activity_redirect"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
