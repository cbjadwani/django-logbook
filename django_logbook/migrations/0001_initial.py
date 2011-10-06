# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LogSummary'
        db.create_table('django_logbook_logsummary', (
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=5, db_index=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=200, null=True, blank=True)),
            ('earliest', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('latest', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('hits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('headline', self.gf('django.db.models.fields.CharField')(default='', max_length=60, blank=True)),
            ('latest_msg', self.gf('django.db.models.fields.TextField')()),
            ('summary_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('django_logbook', ['LogSummary'])

        # Adding model 'Log'
        db.create_table('django_logbook_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=5, db_index=True, blank=True)),
            ('msg', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=200, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='logs', null=True, to=orm['django_logbook.LogSummary'])),
        ))
        db.send_create_signal('django_logbook', ['Log'])


    def backwards(self, orm):
        
        # Deleting model 'LogSummary'
        db.delete_table('django_logbook_logsummary')

        # Deleting model 'Log'
        db.delete_table('django_logbook_log')


    models = {
        'django_logbook.log': {
            'Meta': {'object_name': 'Log'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5', 'db_index': 'True', 'blank': 'True'}),
            'msg': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'blank': 'True'}),
            'summary': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'logs'", 'null': 'True', 'to': "orm['django_logbook.LogSummary']"})
        },
        'django_logbook.logsummary': {
            'Meta': {'ordering': "['-latest']", 'object_name': 'LogSummary'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'earliest': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'blank': 'True'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'latest': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'latest_msg': ('django.db.models.fields.TextField', [], {}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5', 'db_index': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'blank': 'True'}),
            'summary_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['django_logbook']
