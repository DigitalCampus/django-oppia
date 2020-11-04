from django.urls import path

from integrations.xapi import views

app_name = 'xapi'
urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('export/', views.CSVExportView.as_view(), name="export")
]
