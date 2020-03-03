from django.urls import path

from integrations.dhis import views as dhis_views

app_name = 'dhis'
urlpatterns = [
    path('', dhis_views.home, name="index"),
    path('export/latest/', dhis_views.export_latest, name="export_latest"),
    path('export/<int:year>/<int:month>',
         dhis_views.export_month,
         name="export_month")
]
