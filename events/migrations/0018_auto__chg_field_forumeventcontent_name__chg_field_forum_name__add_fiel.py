# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ForumEventContent.name'
        db.alter_column('events_forumeventcontent', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Forum.name'
        db.alter_column('events_forum', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Adding field 'ForumEvent.broadcast_start'
        db.add_column('events_forumevent', 'broadcast_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'ForumEvent.broadcast_end'
        db.add_column('events_forumevent', 'broadcast_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Changing field 'ForumEventContent.name'
        db.alter_column('events_forumeventcontent', 'name', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Changing field 'Forum.name'
        db.alter_column('events_forum', 'name', self.gf('django.db.models.fields.CharField')(max_length=1024))

        # Deleting field 'ForumEvent.broadcast_start'
        db.delete_column('events_forumevent', 'broadcast_start')

        # Deleting field 'ForumEvent.broadcast_end'
        db.delete_column('events_forumevent', 'broadcast_end')


    models = {
        'cms.page': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'object_name': 'Page'},
            'changed_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'menu_login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moderator_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'blank': 'True'}),
            'navigation_extenders': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cms.Page']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Page']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'reverse_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'soft_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
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
            'broadcast_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'broadcast_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'can_register_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_register_youth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['events.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'programm_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {}),
            'title_color': ('django.db.models.fields.CharField', [], {'default': "'blue'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'videostream': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'events.forumeventcontent': {
            'Meta': {'object_name': 'ForumEventContent'},
            'cms_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']", 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_contents'", 'to': "orm['events.ForumEvent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'leader_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'moderators': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'forum_events'", 'null': 'True', 'to': "orm['library.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'library.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'old_person_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['events']
