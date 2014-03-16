# oppia/viz/models.py
from django.db import models
from django.utils.translation import ugettext_lazy as _

class UserLocationVisualization (models.Model):
    ip = models.IPAddressField()
    hits = models.IntegerField(default=0)
    lat = models.FloatField()
    lng = models.FloatField()
    region = models.TextField(blank=True)
    country = models.CharField(max_length=100)
