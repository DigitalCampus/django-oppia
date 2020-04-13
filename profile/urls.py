from django.contrib.auth import views as django_contrib_auth_views
from django.urls import path
from django.views import i18n as django_views_i18n
from django.views.generic import TemplateView

from profile import views as profile_views

app_name = 'profile'

urlpatterns = [
    path('register/', profile_views.register, name="register"),
    path('register/thanks/',
         TemplateView.as_view(template_name="oppia/thanks.html"),
         name="register_thanks"),
    path('login/', profile_views.login_view, name="login"),
    path('logout/',
         django_contrib_auth_views.LogoutView.as_view(),
         {'template_name': 'oppia/logout.html', },
         name="logout"),
    path('setlang/', django_views_i18n.set_language, name="set_language"),
    path('reset/', profile_views.reset, name="reset"),
    path('reset/sent/',
         TemplateView.as_view(template_name="profile/reset-sent.html"),
         name="reset_sent"),
    path('edit/', profile_views.edit, name="edit"),
    path('edit/<int:user_id>/', profile_views.edit, name="edit_user"),
    path('points/', profile_views.points, name="points"),
    path('badges/', profile_views.badges, name="badges"),
    path('<int:user_id>/activity/',
         profile_views.user_activity,
         name="user_activity"),
    path('<int:user_id>/<int:course_id>/activity/',
         profile_views.user_course_activity_view,
         name="user_course_activity"),

    path('<int:user_id>/quizattempts/',
         profile_views.UserAttemptsList.as_view(),
         name="user_all_attempts"),

    path('<int:user_id>/<int:course_id>/quiz/<int:quiz_id>/attempts/',
         profile_views.QuizAttemptsList.as_view(),
         name="user_quiz_attempts"),

    path('<int:user_id>/<int:course_id>/quiz/<int:quiz_id>/attempts/<int:pk>',
         profile_views.QuizAttemptDetail.as_view(),
         name="quiz_attempt_detail"),

    path('upload/', profile_views.UploadUsers.as_view(), name="upload"),
    path('search/', profile_views.search_users, name="search"),
    path('export/', profile_views.export_users, name="export"),
    path('list/', profile_views.list_users, name="list"),

    path('delete/<int:user_id>/', profile_views.delete_account_view, name="delete"),
    path('delete/complete/',
         profile_views.delete_account_complete_view,
         name="delete_complete"),
    path('export/mydata/<data_type>',
         profile_views.export_mydata_view,
         name="export_mydata"),
]
