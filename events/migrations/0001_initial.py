# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Forum'
        db.create_table('events_forum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False, unique=True)),
            ('starts_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('ends_on', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('events', ['Forum'])

        # Adding model 'ForumEvent'
        db.create_table('events_forumevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tags', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Forum'])),
            ('starts_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('ends_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('stream', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
        ))
        db.send_create_signal('events', ['ForumEvent'])


    def backwards(self, orm):
        
        # Deleting model 'Forum'
        db.delete_table('events_forum')

        # Deleting model 'ForumEvent'
        db.delete_table('events_forumevent')


    models = {
        'events.forum': {
            'Meta': {'object_name': 'Forum'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        'events.forumevent': {
            'Meta': {'object_name': 'ForumEvent'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {}),
            'stream': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        }
    }

    complete_apps = ['events']
