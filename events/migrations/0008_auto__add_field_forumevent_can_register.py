# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ForumEvent.can_register'
        db.add_column('events_forumevent', 'can_register', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ForumEvent.can_register'
        db.delete_column('events_forumevent', 'can_register')


    models = {
        'events.forum': {
            'Meta': {'object_name': 'Forum'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ends_on': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'starts_on': ('django.db.models.fields.DateField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        'events.forumevent': {
            'Meta': {'ordering': "['starts_on']", 'object_name': 'ForumEvent'},
            'can_register': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'documents': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_documents'", 'null': 'True', 'to': "orm['history.Category']"}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviews': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_interviews'", 'null': 'True', 'to': "orm['persons.Category']"}),
            'is_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'moderators': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_moderators'", 'null': 'True', 'to': "orm['persons.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_speakers'", 'null': 'True', 'to': "orm['persons.Category']"}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {}),
            'stream': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title_color': ('django.db.models.fields.CharField', [], {'default': "'blue'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        'history.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'persons.category': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'person_template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['events']
