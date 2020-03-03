from django.urls import path

from viz import views as viz_views

app_name = 'viz'

urlpatterns = [
    path('summary/', viz_views.Summary.as_view(), name="summary"),
    path('map/', viz_views.Map.as_view(), name="map"),
]
