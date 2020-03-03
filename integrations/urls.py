from django.conf.urls import include
from django.urls import path

from integrations import views as integration_views

app_name = 'integrations'
urlpatterns = [
    path('', integration_views.home, name="index"),
    path('dhis/', include('integrations.dhis.urls')),
    path('xapi/', include('integrations.xapi.urls')),
]
