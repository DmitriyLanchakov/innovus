# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Forum.starts_on'
        db.alter_column('events_forum', 'starts_on', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Forum.ends_on'
        db.alter_column('events_forum', 'ends_on', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        
        # Changing field 'Forum.starts_on'
        db.alter_column('events_forum', 'starts_on', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Forum.ends_on'
        db.alter_column('events_forum', 'ends_on', self.gf('django.db.models.fields.DateTimeField')())


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
            'Meta': {'object_name': 'ForumEvent'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'moderators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderated'", 'symmetrical': 'False', 'to': "orm['persons.Person']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'speeches'", 'symmetrical': 'False', 'to': "orm['persons.Person']"}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {}),
            'stream': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title_color': ('django.db.models.fields.CharField', [], {'default': "'blue'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
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
        },
        'persons.person': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'Person'},
            'announce': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'persons'", 'symmetrical': 'False', 'to': "orm['persons.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.TextField', [], {}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['persons.Person']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        }
    }

    complete_apps = ['events']
