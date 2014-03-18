# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserLocationVisualization.country'
        db.delete_column(u'viz_userlocationvisualization', 'country')

        # Adding field 'UserLocationVisualization.country_code'
        db.add_column(u'viz_userlocationvisualization', 'country_code',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserLocationVisualization.country_name'
        db.add_column(u'viz_userlocationvisualization', 'country_name',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserLocationVisualization.geonames_data'
        db.add_column(u'viz_userlocationvisualization', 'geonames_data',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'UserLocationVisualization.country'
        db.add_column(u'viz_userlocationvisualization', 'country',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Deleting field 'UserLocationVisualization.country_code'
        db.delete_column(u'viz_userlocationvisualization', 'country_code')

        # Deleting field 'UserLocationVisualization.country_name'
        db.delete_column(u'viz_userlocationvisualization', 'country_name')

        # Deleting field 'UserLocationVisualization.geonames_data'
        db.delete_column(u'viz_userlocationvisualization', 'geonames_data')


    models = {
        u'viz.userlocationvisualization': {
            'Meta': {'object_name': 'UserLocationVisualization'},
            'country_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country_name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'geonames_data': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'region': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['viz']