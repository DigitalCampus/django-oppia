from django.urls import path

from django.views.generic import TemplateView

from activitylog import views as activitylog_views

app_name = 'activitylog'
urlpatterns = [
    path('upload/',
         activitylog_views.upload_view,
         name="upload"),
    path('upload/success/',
         TemplateView.as_view(template_name="activitylog/upload_success.html"),
         name="upload_success"),
]
