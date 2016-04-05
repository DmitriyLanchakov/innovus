# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Category'
        db.create_table('library_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5)),
            ('is_commented', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('library', ['Category'])

        # Adding model 'Person'
        db.create_table('library_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher_is_draft', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('publisher_public', self.gf('django.db.models.fields.related.OneToOneField')(related_name='publisher_draft', unique=True, null=True, to=orm['library.Person'])),
            ('publisher_state', self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5)),
            ('is_commented', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('position', self.gf('django.db.models.fields.TextField')()),
            ('announce', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('old_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('library', ['Person'])

        # Adding M2M table for field categories on 'Person'
        db.create_table('library_person_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['library.person'], null=False)),
            ('category', models.ForeignKey(orm['library.category'], null=False))
        ))
        db.create_unique('library_person_categories', ['person_id', 'category_id'])

        # Adding model 'Resource'
        db.create_table('library_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher_is_draft', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('publisher_public', self.gf('django.db.models.fields.related.OneToOneField')(related_name='publisher_draft', unique=True, null=True, to=orm['library.Resource'])),
            ('publisher_state', self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_commented', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 4, 25, 4, 16, 55, 816955))),
            ('snapshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('library', ['Resource'])

        # Adding M2M table for field category on 'Resource'
        db.create_table('library_resource_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['library.resource'], null=False)),
            ('category', models.ForeignKey(orm['library.category'], null=False))
        ))
        db.create_unique('library_resource_category', ['resource_id', 'category_id'])


    def backwards(self, orm):

        # Deleting model 'Category'
        db.delete_table('library_category')

        # Deleting model 'Person'
        db.delete_table('library_person')

        # Removing M2M table for field categories on 'Person'
        db.delete_table('library_person_categories')

        # Deleting model 'Resource'
        db.delete_table('library_resource')

        # Removing M2M table for field category on 'Resource'
        db.delete_table('library_resource_category')


    models = {
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
        'library.person': {
            'Meta': {'object_name': 'Person'},
            'announce': ('django.db.models.fields.TextField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'persons'", 'symmetrical': 'False', 'to': "orm['library.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.TextField', [], {}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['library.Person']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        'library.resource': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Resource'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'resources'", 'symmetrical': 'False', 'to': "orm['library.Category']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 25, 4, 16, 55, 816955)'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_commented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['library.Resource']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'snapshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['library']

