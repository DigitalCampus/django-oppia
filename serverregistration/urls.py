from django.urls import path
from django.views.generic import TemplateView

from serverregistration import views

app_name = 'serverregistration'

urlpatterns = [
    path('',
         views.RegisterServerView.as_view(),
         name="register"),
    path('thanks/',
         TemplateView.as_view(template_name="serverregistration/thanks.html"),
         name="thanks")
    ]
