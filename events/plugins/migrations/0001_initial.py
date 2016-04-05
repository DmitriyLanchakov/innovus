# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ForumProgramm'
        db.create_table('cmsplugin_forumprogramm', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Forum'])),
            ('program_type', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('plugins', ['ForumProgramm'])

        # Adding model 'PersonsList'
        db.create_table('cmsplugin_personslist', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('block_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('per_page', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('plugins', ['PersonsList'])

        # Adding M2M table for field categories on 'PersonsList'
        db.create_table('plugins_personslist_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('personslist', models.ForeignKey(orm['plugins.personslist'], null=False)),
            ('category', models.ForeignKey(orm['library.category'], null=False))
        ))
        db.create_unique('plugins_personslist_categories', ['personslist_id', 'category_id'])

        # Adding model 'PersonsInCategory'
        db.create_table('cmsplugin_personsincategory', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('block_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('per_page', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lists', to=orm['library.Category'])),
        ))
        db.send_create_signal('plugins', ['PersonsInCategory'])

        # Adding model 'PersonsOnIndex'
        db.create_table('cmsplugin_personsonindex', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('speakers', self.gf('django.db.models.fields.related.ForeignKey')(related_name='speakers', to=orm['library.Category'])),
            ('speakers_count', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('interviews', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interviews', to=orm['library.Category'])),
            ('interviews_count', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('plugins', ['PersonsOnIndex'])

        # Adding model 'Toggle'
        db.create_table('cmsplugin_toggle', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('plugins', ['Toggle'])

        # Adding model 'Menu'
        db.create_table('cmsplugin_menu', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('from_level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('to_level', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            ('extra_inactive', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('extra_active', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
            ('root_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='menu/extralevel_navigation.html', max_length=255)),
        ))
        db.send_create_signal('plugins', ['Menu'])

        # Adding model 'Sitemap'
        db.create_table('cmsplugin_sitemap', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('plugins', ['Sitemap'])

        # Adding model 'PageCategory'
        db.create_table('cmsplugin_pagecategory', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['periodics.Category'])),
            ('is_commented', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('per_page', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('plugins', ['PageCategory'])

        # Adding model 'LastPosts'
        db.create_table('cmsplugin_lastposts', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('posts_count', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('plugins', ['LastPosts'])

        # Adding M2M table for field categories on 'LastPosts'
        db.create_table('plugins_lastposts_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lastposts', models.ForeignKey(orm['plugins.lastposts'], null=False)),
            ('category', models.ForeignKey(orm['periodics.category'], null=False))
        ))
        db.create_unique('plugins_lastposts_categories', ['lastposts_id', 'category_id'])

        # Adding model 'LastComments'
        db.create_table('cmsplugin_lastcomments', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('comments_count', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('plugins', ['LastComments'])

        # Adding model 'LastVideo'
        db.create_table('cmsplugin_lastvideo', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['periodics.Category'])),
        ))
        db.send_create_signal('plugins', ['LastVideo'])

        # Adding model 'Innonews'
        db.create_table('cmsplugin_innonews', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('world', self.gf('django.db.models.fields.related.ForeignKey')(related_name='innonews_world', to=orm['periodics.Category'])),
            ('russia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='innonews_russia', to=orm['periodics.Category'])),
            ('tomsk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='innonews_tomsk', to=orm['periodics.Category'])),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('plugins', ['Innonews'])


    def backwards(self, orm):
        
        # Deleting model 'ForumProgramm'
        db.delete_table('cmsplugin_forumprogramm')

        # Deleting model 'PersonsList'
        db.delete_table('cmsplugin_personslist')

        # Removing M2M table for field categories on 'PersonsList'
        db.delete_table('plugins_personslist_categories')

        # Deleting model 'PersonsInCategory'
        db.delete_table('cmsplugin_personsincategory')

        # Deleting model 'PersonsOnIndex'
        db.delete_table('cmsplugin_personsonindex')

        # Deleting model 'Toggle'
        db.delete_table('cmsplugin_toggle')

        # Deleting model 'Menu'
        db.delete_table('cmsplugin_menu')

        # Deleting model 'Sitemap'
        db.delete_table('cmsplugin_sitemap')

        # Deleting model 'PageCategory'
        db.delete_table('cmsplugin_pagecategory')

        # Deleting model 'LastPosts'
        db.delete_table('cmsplugin_lastposts')

        # Removing M2M table for field categories on 'LastPosts'
        db.delete_table('plugins_lastposts_categories')

        # Deleting model 'LastComments'
        db.delete_table('cmsplugin_lastcomments')

        # Deleting model 'LastVideo'
        db.delete_table('cmsplugin_lastvideo')

        # Deleting model 'Innonews'
        db.delete_table('cmsplugin_innonews')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
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
        'library.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'periodics.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.CharField', [], {'default': "'script'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'post_template': ('django.db.models.fields.CharField', [], {'default': "'post-single.html'", 'max_length': "'255'"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'plugins.forumprogramm': {
            'Meta': {'object_name': 'ForumProgramm', 'db_table': "'cmsplugin_forumprogramm'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Forum']"}),
            'program_type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'plugins.innonews': {
            'Meta': {'object_name': 'Innonews', 'db_table': "'cmsplugin_innonews'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'russia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'innonews_russia'", 'to': "orm['periodics.Category']"}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tomsk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'innonews_tomsk'", 'to': "orm['periodics.Category']"}),
            'world': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'innonews_world'", 'to': "orm['periodics.Category']"})
        },
        'plugins.lastcomments': {
            'Meta': {'object_name': 'LastComments', 'db_table': "'cmsplugin_lastcomments'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'plugins.lastposts': {
            'Meta': {'object_name': 'LastPosts', 'db_table': "'cmsplugin_lastposts'", '_ormbases': ['cms.CMSPlugin']},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['periodics.Category']", 'symmetrical': 'False'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'posts_count': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'plugins.lastvideo': {
            'Meta': {'object_name': 'LastVideo', 'db_table': "'cmsplugin_lastvideo'", '_ormbases': ['cms.CMSPlugin']},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['periodics.Category']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        'plugins.menu': {
            'Meta': {'object_name': 'Menu', 'db_table': "'cmsplugin_menu'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'extra_active': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'extra_inactive': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'from_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'root_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'menu/extralevel_navigation.html'", 'max_length': '255'}),
            'to_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'})
        },
        'plugins.pagecategory': {
            'Meta': {'object_name': 'PageCategory', 'db_table': "'cmsplugin_pagecategory'", '_ormbases': ['cms.CMSPlugin']},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['periodics.Category']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'plugins.personsincategory': {
            'Meta': {'object_name': 'PersonsInCategory', 'db_table': "'cmsplugin_personsincategory'", '_ormbases': ['cms.CMSPlugin']},
            'block_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lists'", 'to': "orm['library.Category']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'plugins.personslist': {
            'Meta': {'object_name': 'PersonsList', 'db_table': "'cmsplugin_personslist'", '_ormbases': ['cms.CMSPlugin']},
            'block_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'persons_plugin_categories'", 'symmetrical': 'False', 'to': "orm['library.Category']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'plugins.personsonindex': {
            'Meta': {'object_name': 'PersonsOnIndex', 'db_table': "'cmsplugin_personsonindex'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'interviews': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['library.Category']"}),
            'interviews_count': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'speakers': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'speakers'", 'to': "orm['library.Category']"}),
            'speakers_count': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'plugins.sitemap': {
            'Meta': {'object_name': 'Sitemap', 'db_table': "'cmsplugin_sitemap'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'plugins.toggle': {
            'Meta': {'object_name': 'Toggle', 'db_table': "'cmsplugin_toggle'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['plugins']
