# oppia/activitylog/models.py
import datetime
import os 

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UploadedActivityLog(models.Model):
    
    create_user = models.ForeignKey(User, related_name='activitylog_create_user')
    created_date = models.DateTimeField('date created',default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated',default=timezone.now)
    file = models.FileField(upload_to="activitylog/%Y/%m/",blank=False)
    
    class Meta:
        verbose_name = _(u'Uploaded Activity Log')
        verbose_name_plural = _(u'Uploaded Activity Log')
     
    def __unicode__(self):
        return self.file.name