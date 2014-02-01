# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tracker.activity_title'
        db.add_column(u'oppia_tracker', 'activity_title',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tracker.activity_title'
        db.delete_column(u'oppia_tracker', 'activity_title')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'oppia.activity': {
            'Meta': {'object_name': 'Activity'},
            'baseline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Section']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'oppia.activityschedule': {
            'Meta': {'object_name': 'ActivitySchedule'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Schedule']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'oppia.award': {
            'Meta': {'object_name': 'Award'},
            'award_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Badge']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oppia.awardcourse': {
            'Meta': {'object_name': 'AwardCourse'},
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Award']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'course_version': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'oppia.badge': {
            'Meta': {'object_name': 'Badge'},
            'allow_multiple_awards': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default_icon': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'oppia.cohort': {
            'Meta': {'object_name': 'Cohort'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['oppia.Schedule']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'oppia.course': {
            'Meta': {'object_name': 'Course'},
            'badge_icon': ('django.db.models.fields.files.FileField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastupdated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'version': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'oppia.coursedownload': {
            'Meta': {'object_name': 'CourseDownload'},
            'agent': ('django.db.models.fields.TextField', [], {'default': 'None', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'course_version': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'download_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oppia.coursetag': {
            'Meta': {'object_name': 'CourseTag'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Tag']"})
        },
        u'oppia.media': {
            'Meta': {'object_name': 'Media'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'download_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'oppia.message': {
            'Meta': {'object_name': 'Message'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'oppia.participant': {
            'Meta': {'object_name': 'Participant'},
            'cohort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Cohort']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oppia.points': {
            'Meta': {'object_name': 'Points'},
            'cohort': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Cohort']", 'null': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']", 'null': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oppia.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'oppia.section': {
            'Meta': {'object_name': 'Section'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'oppia.tag': {
            'Meta': {'object_name': 'Tag'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oppia.Course']", 'through': u"orm['oppia.CourseTag']", 'symmetrical': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'oppia.tracker': {
            'Meta': {'object_name': 'Tracker'},
            'activity_title': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'agent': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['oppia.Course']", 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'submitted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'time_taken': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tracker_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['oppia']