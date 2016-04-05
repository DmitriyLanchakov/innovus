# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
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
        
        # Deleting model 'Innonews'
        db.delete_table('cmsplugin_innonews')



    complete_apps = ['plugins']
