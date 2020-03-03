from django.urls import path

from integrations.xapi import views as xapi_views

app_name = 'xapi'
urlpatterns = [
    path('', xapi_views.home, name="index"),
    path('export/', xapi_views.csv_export, name="export")
]
