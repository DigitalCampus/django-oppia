from django.urls import path

from integrations.dhis import views

app_name = 'dhis'
urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('export/latest/',
         views.ExportLatestView.as_view(),
         name="export_latest"),
    path('export/<int:year>/<int:month>',
         views.ExportMonthView.as_view(),
         name="export_month")
]
