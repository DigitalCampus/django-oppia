# oppia/av/models.py
import datetime
import hashlib
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

EMBED_TEMPLATE = "[[media object='{\"filename\":\"%s\", \"download_url\":\"%s\", \"digest\":\"%s\", \"filesize\":%d, \"length\":%d}']]IMAGE/TEXT HERE[[/media]]"


class UploadedMedia(models.Model):

    UPLOAD_STATUS_SUCCESS = 1
    UPLOAD_STATUS_EXISTS = 2
    UPLOAD_STATUS_FAILURE = 0

    create_user = models.ForeignKey(User, related_name='media_create_user', null=True, on_delete=models.SET_NULL)
    update_user = models.ForeignKey(User, related_name='media_update_user', null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated', default=timezone.now)
    file = models.FileField(upload_to="uploaded/%Y/%m/", blank=False)
    md5 = models.CharField(max_length=100)
    length = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Uploaded Media')
        verbose_name_plural = _(u'Uploaded Media')

    def __unicode__(self):
        return self.file.name

    def get_embed_code(self, uri):
        return EMBED_TEMPLATE % (os.path.basename(self.file.name), uri, self.md5, self.file.size, self.length)

    def filename(self):
        return os.path.basename(self.file.name)

    def get_default_image(self):
        try:
            img = UploadedMediaImage.objects.get(uploaded_media=self, default_image=True)
            return img
        except UploadedMediaImage.DoesNotExist:
            try:
                img = UploadedMediaImage.objects.filter(uploaded_media=self).order_by('created_date').first()
                return img
            except UploadedMediaImage.DoesNotExist:
                return None


@receiver(post_delete, sender=UploadedMedia)
def uploaded_media_delete_file(sender, instance, **kwargs):
    file_to_delete = os.path.join(settings.MEDIA_ROOT, instance.file.name)
    print("deleting ...." + file_to_delete)
    try:
        os.remove(file_to_delete)
        print("File removed")
    except OSError:
        print("Error deleting media")


def image_file_name(instance, filename):
    return os.path.join('uploaded/images', filename[0:2], filename[2:4], filename)

       
class UploadedMediaImage(models.Model):

    create_user = models.ForeignKey(User, related_name='media_image_create_user', null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField('date created', default=timezone.now)
    image = models.ImageField(upload_to=image_file_name, blank=False)
    uploaded_media = models.ForeignKey(UploadedMedia, on_delete=models.CASCADE, related_name='images')
    default_image = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'Uploaded Media Image')
        verbose_name_plural = _(u'Uploaded Media Images')

    def __unicode__(self):
        return self.image.name


@receiver(post_delete, sender=UploadedMediaImage)
def uploaded_media_image_delete_file(sender, instance, **kwargs):
    image_to_delete = os.path.join(settings.MEDIA_ROOT, instance.image.name)
    print("deleting ...." + image_to_delete)
    try:
        os.remove(image_to_delete)
        print("Image removed")
    except OSError:
        print("Error deleting image")
