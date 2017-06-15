# oppia/av/admin.py
from django.contrib import admin
from oppia.av.models import UploadedMedia

class UploadedMediaAdmin(admin.ModelAdmin):
    list_display = ('course_shortname', 'file', 'image', 'created_date', 'md5', 'length')
    
    
admin.site.register(UploadedMedia, UploadedMediaAdmin)  
    