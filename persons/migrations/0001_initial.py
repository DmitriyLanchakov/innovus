# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('persons_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5)),
            ('is_commented', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('person_template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('persons', ['Category'])

        # Adding model 'Person'
        db.create_table('persons_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher_is_draft', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('publisher_public', self.gf('django.db.models.fields.related.OneToOneField')(related_name='publisher_draft', unique=True, null=True, to=orm['persons.Person'])),
            ('publisher_state', self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5)),
            ('is_commented', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('position', self.gf('django.db.models.fields.TextField')()),
            ('announce', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('photo_w', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('photo_h', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('persons', ['Person'])

        # Adding M2M table for field category on 'Person'
        db.create_table('persons_person_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['persons.person'], null=False)),
            ('category', models.ForeignKey(orm['persons.category'], null=False))
        ))
        db.create_unique('persons_person_category', ['person_id', 'category_id'])

        # Adding model 'Persons'
        db.create_table('cmsplugin_persons', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('block_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('per_page', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('persons', ['Persons'])

        # Adding M2M table for field categories on 'Persons'
        db.create_table('persons_persons_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persons', models.ForeignKey(orm['persons.persons'], null=False)),
            ('category', models.ForeignKey(orm['persons.category'], null=False))
        ))
        db.create_unique('persons_persons_categories', ['persons_id', 'category_id'])

        # Adding model 'PersonList'
        db.create_table('cmsplugin_personlist', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('block_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('per_page', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lists', to=orm['persons.Category'])),
        ))
        db.send_create_signal('persons', ['PersonList'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('persons_category')

        # Deleting model 'Person'
        db.delete_table('persons_person')

        # Removing M2M table for field category on 'Person'
        db.delete_table('persons_person_category')

        # Deleting model 'Persons'
        db.delete_table('cmsplugin_persons')

        # Removing M2M table for field categories on 'Persons'
        db.delete_table('persons_persons_categories')

        # Deleting model 'PersonList'
        db.delete_table('cmsplugin_personlist')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photo_h': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'photo_w': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'position': ('django.db.models.fields.TextField', [], {}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['persons.Person']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'persons.personlist': {
            'Meta': {'object_name': 'PersonList', 'db_table': "'cmsplugin_personlist'", '_ormbases': ['cms.CMSPlugin']},
            'block_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lists'", 'to': "orm['persons.Category']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'persons.persons': {
            'Meta': {'object_name': 'Persons', 'db_table': "'cmsplugin_persons'", '_ormbases': ['cms.CMSPlugin']},
            'block_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'catz'", 'symmetrical': 'False', 'to': "orm['persons.Category']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['persons']
