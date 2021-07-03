
from django.contrib import admin

from av.models import UploadedMedia


class UploadedMediaAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'file',
                    'created_date',
                    'md5',
                    'length',
                    'title',
                    'organisation',
                    'license')


admin.site.register(UploadedMedia, UploadedMediaAdmin)
