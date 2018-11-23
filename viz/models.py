# oppia/viz/models.py
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserLocationVisualization (models.Model):
    ip = models.GenericIPAddressField()
    hits = models.IntegerField(default=0)
    lat = models.FloatField()
    lng = models.FloatField()
    region = models.TextField(blank=True)
    country_code = models.CharField(max_length=100, blank=True, null=True, default=None)
    country_name = models.TextField(blank=True, null=True, default=None)
    geonames_data = models.TextField(blank=True, null=True, default=None)
