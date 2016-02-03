# oppia/reports/models.py

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class DashboardAccessLog (models.Model):
    user = models.ForeignKey(User,null=True, blank=True, default=None, on_delete=models.SET_NULL)
    access_date = models.DateTimeField('date created',default=timezone.now)
    ip = models.GenericIPAddressField(blank=True, null=True, default=None)
    agent = models.TextField(blank=True, null=True, default=None)
    url = models.TextField(blank=True, null=True, default=None)
    data = models.TextField(blank=True, null=True, default=None)
    
    
    