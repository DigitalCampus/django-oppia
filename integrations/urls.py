from django.conf.urls import include
from django.urls import path

from integrations import views

app_name = 'integrations'
urlpatterns = [
    path('', views.HomeView.as_view(), name="index"),
    path('dhis/', include('integrations.dhis.urls')),
    path('xapi/', include('integrations.xapi.urls')),
]
