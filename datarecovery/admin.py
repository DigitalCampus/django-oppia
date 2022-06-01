from django.contrib import admin

from datarecovery.models import DataRecovery


@admin.register(DataRecovery)
class DataRecoveryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date', 'data_type', 'reasons', 'data', 'recovered')
