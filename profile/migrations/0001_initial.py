# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('profile_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('alpha2', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('alpha3', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('iso', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('profile', ['Country'])

        # Adding model 'Region'
        db.create_table('profile_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regions', to=orm['profile.Country'])),
        ))
        db.send_create_signal('profile', ['Region'])

        # Adding model 'City'
        db.create_table('profile_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cities', to=orm['profile.Country'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cities', to=orm['profile.Region'])),
        ))
        db.send_create_signal('profile', ['City'])

        # Adding model 'Industry'
        db.create_table('profile_industry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal('profile', ['Industry'])

        # Adding model 'Claim'
        db.create_table('profile_claim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='claims', null=True, to=orm['profile.Country'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='claims', null=True, to=orm['profile.Region'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='claims', null=True, to=orm['profile.City'])),
            ('delegation_manager', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='delegates', null=True, to=orm['profile.Claim'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='claims', null=True, to=orm['auth.User'])),
            ('activation_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('bill', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('bill_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('citizenship', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('claim_state', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.IntegerField')()),
            ('is_take_part', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('phone_extra', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('icq', self.gf('django.db.models.fields.CharField')(default='', max_length=9, blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(default='', max_length=255, blank=True)),
            ('blog', self.gf('django.db.models.fields.URLField')(default='', max_length=255, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('need_hotel', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('claim_type', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='claims', null=True, to=orm['profile.Industry'])),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('arrival_want_charter', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('arrival_transport_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('arrival_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('departure_want_charter', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('departure_transport_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('departure_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_synchronized', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('additional_info', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('payment_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_sum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('is_registered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_invited', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('profile', ['Claim'])

        # Adding model 'History'
        db.create_table('profile_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('claim', self.gf('django.db.models.fields.related.ForeignKey')(related_name='histories', null=True, to=orm['profile.Claim'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='histories', null=True, to=orm['auth.User'])),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value_before', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('value_after', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('profile', ['History'])

        # Adding model 'Registration'
        db.create_table('cmsplugin_registration', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('profile', ['Registration'])

        # Adding model 'Participants'
        db.create_table('cmsplugin_participants', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('per_page', self.gf('django.db.models.fields.IntegerField')(default=10, blank=True)),
        ))
        db.send_create_signal('profile', ['Participants'])

        # Adding model 'Hotel'
        db.create_table('profile_hotel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('profile', ['Hotel'])

        # Adding model 'HotelRoomCategory'
        db.create_table('profile_hotelroomcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hotel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='room_categories', to=orm['profile.Hotel'])),
            ('room_category', self.gf('django.db.models.fields.IntegerField')()),
            ('room_number', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('is_real_room', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('profile', ['HotelRoomCategory'])

        # Adding model 'HotelRoomReserve'
        db.create_table('profile_hotelroomreserve', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hotel_reserves', to=orm['profile.HotelRoomCategory'])),
            ('claim', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hotel_reserves', to=orm['profile.Claim'])),
            ('arrival_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('departure_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('profile', ['HotelRoomReserve'])

        # Adding model 'Event'
        db.create_table('profile_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_started', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('date_finished', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('annotation', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('annotation_en', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('place', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('place_en', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('can_register', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('broadcast_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_displayable', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('profile', ['Event'])

        # Adding model 'Events'
        db.create_table('cmsplugin_events', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(max_length=255)),
        ))
        db.send_create_signal('profile', ['Events'])

        # Adding model 'EventsNow'
        db.create_table('cmsplugin_eventsnow', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('profile', ['EventsNow'])

        # Adding model 'ClaimEvent'
        db.create_table('profile_claimevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('claim', self.gf('django.db.models.fields.related.ForeignKey')(related_name='claim_events', to=orm['profile.Claim'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='claim_events', to=orm['profile.Event'])),
        ))
        db.send_create_signal('profile', ['ClaimEvent'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('profile_country')

        # Deleting model 'Region'
        db.delete_table('profile_region')

        # Deleting model 'City'
        db.delete_table('profile_city')

        # Deleting model 'Industry'
        db.delete_table('profile_industry')

        # Deleting model 'Claim'
        db.delete_table('profile_claim')

        # Deleting model 'History'
        db.delete_table('profile_history')

        # Deleting model 'Registration'
        db.delete_table('cmsplugin_registration')

        # Deleting model 'Participants'
        db.delete_table('cmsplugin_participants')

        # Deleting model 'Hotel'
        db.delete_table('profile_hotel')

        # Deleting model 'HotelRoomCategory'
        db.delete_table('profile_hotelroomcategory')

        # Deleting model 'HotelRoomReserve'
        db.delete_table('profile_hotelroomreserve')

        # Deleting model 'Event'
        db.delete_table('profile_event')

        # Deleting model 'Events'
        db.delete_table('cmsplugin_events')

        # Deleting model 'EventsNow'
        db.delete_table('cmsplugin_eventsnow')

        # Deleting model 'ClaimEvent'
        db.delete_table('profile_claimevent')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profile.city': {
            'Meta': {'ordering': "('title',)", 'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['profile.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['profile.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'profile.claim': {
            'Meta': {'object_name': 'Claim'},
            'activation_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'additional_info': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'arrival_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'arrival_transport_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'arrival_want_charter': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'bill': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'bill_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'blog': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'citizenship': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claims'", 'null': 'True', 'to': "orm['profile.City']"}),
            'claim_state': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'claim_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claims'", 'null': 'True', 'to': "orm['profile.Country']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'delegation_manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'delegates'", 'null': 'True', 'to': "orm['profile.Claim']"}),
            'departure_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'departure_transport_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'departure_want_charter': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.IntegerField', [], {}),
            'icq': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '9', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claims'", 'null': 'True', 'to': "orm['profile.Industry']"}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_synchronized': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_take_part': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'need_hotel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'payment_sum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone_extra': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claims'", 'null': 'True', 'to': "orm['profile.Region']"}),
            'site': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'claims'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'profile.claimevent': {
            'Meta': {'object_name': 'ClaimEvent'},
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claim_events'", 'to': "orm['profile.Claim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claim_events'", 'to': "orm['profile.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'profile.country': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Country'},
            'alpha2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'alpha3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'profile.event': {
            'Meta': {'ordering': "['date_started', 'sort_order']", 'object_name': 'Event'},
            'annotation': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'annotation_en': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'broadcast_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'can_register': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'date_finished': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'event_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_displayable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'place_en': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'profile.events': {
            'Meta': {'object_name': 'Events', 'db_table': "'cmsplugin_events'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'profile.eventsnow': {
            'Meta': {'object_name': 'EventsNow', 'db_table': "'cmsplugin_eventsnow'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'profile.history': {
            'Meta': {'object_name': 'History'},
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'histories'", 'null': 'True', 'to': "orm['profile.Claim']"}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'histories'", 'null': 'True', 'to': "orm['auth.User']"}),
            'value_after': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_before': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'profile.hotel': {
            'Meta': {'ordering': "['name']", 'object_name': 'Hotel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'profile.hotelroomcategory': {
            'Meta': {'object_name': 'HotelRoomCategory'},
            'hotel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room_categories'", 'to': "orm['profile.Hotel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_real_room': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'room_category': ('django.db.models.fields.IntegerField', [], {}),
            'room_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'profile.hotelroomreserve': {
            'Meta': {'object_name': 'HotelRoomReserve'},
            'arrival_date': ('django.db.models.fields.DateTimeField', [], {}),
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hotel_reserves'", 'to': "orm['profile.Claim']"}),
            'departure_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hotel_reserves'", 'to': "orm['profile.HotelRoomCategory']"})
        },
        'profile.industry': {
            'Meta': {'ordering': "['sort_order', 'title', 'title_en']", 'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'profile.participants': {
            'Meta': {'object_name': 'Participants', 'db_table': "'cmsplugin_participants'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'per_page': ('django.db.models.fields.IntegerField', [], {'default': '10', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'profile.region': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Region'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': "orm['profile.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'profile.registration': {
            'Meta': {'object_name': 'Registration', 'db_table': "'cmsplugin_registration'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['profile']
