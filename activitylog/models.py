# oppia/activitylog/models.py
import datetime
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UploadedActivityLog(models.Model):

    create_user = models.ForeignKey(User, related_name='activitylog_create_user', on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated', default=timezone.now)
    file = models.FileField(upload_to="activitylog/%Y/%m/", blank=False)

    class Meta:
        verbose_name = _(u'Uploaded Activity Log')
        verbose_name_plural = _(u'Uploaded Activity Log')

    def __unicode__(self):
        return self.file.name

    
@receiver(post_delete, sender=UploadedActivityLog)
def activity_log_delete_file(sender, instance, **kwargs):
    file_to_delete = instance.file.path
    print("deleting ...." + file_to_delete)
    os.remove(file_to_delete)
    print("File removed")
