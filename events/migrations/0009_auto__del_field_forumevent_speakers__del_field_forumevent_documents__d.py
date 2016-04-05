# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ForumEvent.speakers'
        db.delete_column('events_forumevent', 'speakers_id')

        # Deleting field 'ForumEvent.documents'
        db.delete_column('events_forumevent', 'documents_id')

        # Deleting field 'ForumEvent.event_type'
        db.delete_column('events_forumevent', 'event_type')

        # Deleting field 'ForumEvent.stream'
        db.delete_column('events_forumevent', 'stream')

        # Deleting field 'ForumEvent.interviews'
        db.delete_column('events_forumevent', 'interviews_id')

        # Deleting field 'ForumEvent.content'
        db.delete_column('events_forumevent', 'content')

        # Deleting field 'ForumEvent.is_link'
        db.delete_column('events_forumevent', 'is_link')

        # Adding field 'ForumEvent.programm_type'
        db.add_column('events_forumevent', 'programm_type', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'ForumEvent.cms_page'
        db.add_column('events_forumevent', 'cms_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'ForumEvent.speakers'
        db.add_column('events_forumevent', 'speakers', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_speakers', null=True, to=orm['persons.Category'], blank=True), keep_default=False)

        # Adding field 'ForumEvent.documents'
        db.add_column('events_forumevent', 'documents', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_documents', null=True, to=orm['history.Category'], blank=True), keep_default=False)

        # Adding field 'ForumEvent.event_type'
        db.add_column('events_forumevent', 'event_type', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Adding field 'ForumEvent.stream'
        db.add_column('events_forumevent', 'stream', self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True), keep_default=False)

        # Adding field 'ForumEvent.interviews'
        db.add_column('events_forumevent', 'interviews', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_interviews', null=True, to=orm['persons.Category'], blank=True), keep_default=False)

        # Adding field 'ForumEvent.content'
        db.add_column('events_forumevent', 'content', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'ForumEvent.is_link'
        db.add_column('events_forumevent', 'is_link', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'ForumEvent.programm_type'
        db.delete_column('events_forumevent', 'programm_type')

        # Deleting field 'ForumEvent.cms_page'
        db.delete_column('events_forumevent', 'cms_page_id')


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
            'can_register': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cms_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'moderators': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_moderators'", 'null': 'True', 'to': "orm['persons.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'programm_type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {}),
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
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['events']
