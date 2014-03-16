# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserLocationVisualization'
        db.create_table(u'viz_userlocationvisualization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('hits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('region', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'viz', ['UserLocationVisualization'])


    def backwards(self, orm):
        # Deleting model 'UserLocationVisualization'
        db.delete_table(u'viz_userlocationvisualization')


    models = {
        u'viz.userlocationvisualization': {
            'Meta': {'object_name': 'UserLocationVisualization'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'region': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['viz']