from django.urls import path
from serverregistration import views

app_name = 'serverregistration'

urlpatterns = [
    path('',
         views.RegisterServerView.as_view(),
         name="register")
    ]