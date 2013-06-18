# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'oppia_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lastupdated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('version', self.gf('django.db.models.fields.BigIntegerField')()),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('badge_icon', self.gf('django.db.models.fields.files.FileField')(default=None, max_length=100, blank=True)),
        ))
        db.send_create_signal(u'oppia', ['Course'])

        # Adding model 'Tag'
        db.create_table(u'oppia_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'oppia', ['Tag'])

        # Adding model 'CourseTag'
        db.create_table(u'oppia_coursetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Tag'])),
        ))
        db.send_create_signal(u'oppia', ['CourseTag'])

        # Adding model 'Schedule'
        db.create_table(u'oppia_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('lastupdated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'oppia', ['Schedule'])

        # Adding model 'ActivitySchedule'
        db.create_table(u'oppia_activityschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Schedule'])),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'oppia', ['ActivitySchedule'])

        # Adding model 'Section'
        db.create_table(u'oppia_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'oppia', ['Section'])

        # Adding model 'Activity'
        db.create_table(u'oppia_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Section'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'oppia', ['Activity'])

        # Adding model 'Media'
        db.create_table(u'oppia_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('download_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'oppia', ['Media'])

        # Adding model 'Tracker'
        db.create_table(u'oppia_tracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('submitted_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('tracker_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('agent', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['oppia.Course'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_taken', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'oppia', ['Tracker'])

        # Adding model 'CourseDownload'
        db.create_table(u'oppia_coursedownload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('download_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('course_version', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal(u'oppia', ['CourseDownload'])

        # Adding model 'Cohort'
        db.create_table(u'oppia_cohort', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['oppia.Schedule'], null=True, blank=True)),
        ))
        db.send_create_signal(u'oppia', ['Cohort'])

        # Adding model 'Participant'
        db.create_table(u'oppia_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cohort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Cohort'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'oppia', ['Participant'])

        # Adding model 'Message'
        db.create_table(u'oppia_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'oppia', ['Message'])

        # Adding model 'Badge'
        db.create_table(u'oppia_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('default_icon', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('allow_multiple_awards', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'oppia', ['Badge'])

        # Adding model 'Award'
        db.create_table(u'oppia_award', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Badge'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('award_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'oppia', ['Award'])

        # Adding model 'AwardCourse'
        db.create_table(u'oppia_awardcourse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('award', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Award'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'])),
            ('course_version', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal(u'oppia', ['AwardCourse'])

        # Adding model 'Points'
        db.create_table(u'oppia_points', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Course'], null=True)),
            ('cohort', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oppia.Cohort'], null=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'oppia', ['Points'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'oppia_course')

        # Deleting model 'Tag'
        db.delete_table(u'oppia_tag')

        # Deleting model 'CourseTag'
        db.delete_table(u'oppia_coursetag')

        # Deleting model 'Schedule'
        db.delete_table(u'oppia_schedule')

        # Deleting model 'ActivitySchedule'
        db.delete_table(u'oppia_activityschedule')

        # Deleting model 'Section'
        db.delete_table(u'oppia_section')

        # Deleting model 'Activity'
        db.delete_table(u'oppia_activity')

        # Deleting model 'Media'
        db.delete_table(u'oppia_media')

        # Deleting model 'Tracker'
        db.delete_table(u'oppia_tracker')

        # Deleting model 'CourseDownload'
        db.delete_table(u'oppia_coursedownload')

        # Deleting model 'Cohort'
        db.delete_table(u'oppia_cohort')

        # Deleting model 'Participant'
        db.delete_table(u'oppia_participant')

        # Deleting model 'Message'
        db.delete_table(u'oppia_message')

        # Deleting model 'Badge'
        db.delete_table(u'oppia_badge')

        # Deleting model 'Award'
        db.delete_table(u'oppia_award')

        # Deleting model 'AwardCourse'
        db.delete_table(u'oppia_awardcourse')

        # Deleting model 'Points'
        db.delete_table(u'oppia_points')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'lastupdated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'version': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'oppia.coursedownload': {
            'Meta': {'object_name': 'CourseDownload'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oppia.Course']"}),
            'course_version': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'download_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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