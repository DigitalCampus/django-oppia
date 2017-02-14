# oppia/av/models.py
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UploadedMedia(models.Model):
    course_shortname = models.CharField(max_length=100)
    create_user = models.ForeignKey(User, related_name='media_create_user')
    update_user = models.ForeignKey(User, related_name='media_update_user')
    created_date = models.DateTimeField('date created',default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated',default=timezone.now)
    file = models.FileField(upload_to="uploaded",blank=False)
    image = models.FileField(upload_to="uploaded",blank=True, default=None)
    md5 = models.CharField(max_length=100)
    length = models.IntegerField(default=0, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Uploaded Media')
        verbose_name_plural = _('Uploaded Media')
        
    #def __unicode__(self):
    #    return self.get_title(self)