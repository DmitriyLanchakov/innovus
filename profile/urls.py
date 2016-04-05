# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('profile.views',
    # Main
    # View profile
    url(
      regex = "^$",
      view = "participant.view",
      name = "profile_view",
    ),
    # participant registration:
    url(
      regex = "^join/$",
      view = "participant.add",
      name = "join_participant",
    ),
    url(
      regex = "^edit/$",
      view = "participant.edit",
      name = "edit_participant"
    ),
    # contact person registration:
    url(
        regex = "^contact/join/$",
        view  = 'contact.add',
        name  = 'join_contact',
    ),
    url(
        regex = "^contact/edit/(?P<id>\d+)/$",
        view  = 'contact.edit',
        name  = 'edit_contact',
    ),
    # Delegation management
    url(
        regex = "^delegate/join/$",
        view = "delegate.add",
        name = "add_delegate",
    ),
    url(
        regex = "^delegate/list/$",
        view = "delegate.list",
        name = "list_delegate",
    ),
    url(
        regex = "^delegate/show/(?P<id>\d+)/$",
        view = "delegate.show",
        name = "show_delegate",
    ),
    url(
        regex = '^delegate/edit/(?P<id>\d+)/$',
        view  = 'delegate.edit',
        name  = 'edit_delegate',
    ),
    url(
        regex = '^delegate/delete/(?P<id>\d+)/delete/$',
        view  = 'delegate.delete',
        name  = 'delete_delegate',
    ),

    url(
        regex = '^region/filter/$',
        view  = 'ajax.regions_filter',
        name  = 'profile_ajax_region_filter',
    ),
    url(
        regex = '^hotel/classes/(?P<id>\d+)/$',
        view  = 'ajax.get_hotel_categories',
        name  = 'ajax_get_hotel_categories',
    ),
    url(
        regex = '^hotel/classes/(?P<hotel_id>\d+)/(?P<cat_id>\d+)/$',
        view  = 'ajax.get_room_by_categy',
        name  = 'ajax_get_room_by_categy',
    ),
    url(
        regex = '^activation/$',
        view  = 'account.activation',
        name  = 'profile_activation',
    ),

    url(
        regex = '^activation/(?P<code>.*?)/$',
        view  = 'account.activation',
        name = 'profile_activation',
    ),
    url(
        regex = '^cancel/$',
        view  = 'account.cancel',
        name  = 'cancel_claim',
    ),
    url(
        regex = '^cancel/(?P<id>\d+)/$',
        view  = 'account.cancel',
        name  = 'cancel_claim2',
    ),
    url(
        regex = '^bill/(?P<id>\d+)/$',
        view  = 'account.get_bill',
        name  = 'profile_bill',
    ),



    ##
    ## Claims in events
   ##

    ##
    ## MANAGEMENT
    ##
    url(
        regex = '^management/statistics/registered/$',
        view  = 'statistics.registration',
        name  = 'statistics_registered',
    ),
    url(
        regex = '^management/settlers_list/$',
        view  = 'management_old.settlers_list',
        name  = 'manage_settlers_list',
    ),
    url(
        regex = '^management/claims_by_countries/$',
        view  = 'management_old.by_countries',
        name  = 'claims_by_countries',
    ),
    url(
        regex = '^management/claims_by_regions/$',
        view  = 'management_old.by_regions',
        name  = 'claims_by_regions',
    ),

    url(
        regex = '^management/change_state/(?P<id>\d+)/$',
        view  = 'management_old.state_change',
        name  = 'manage_state_change',
    ),
    url(
        regex = '^management/request_process/(?P<id>\d+)/$',
        view  = 'actions.request_process',
        name  = 'actions_request_process',
    ),
    url(
        regex = '^management/registration_process/(?P<id>\d+)/$',
        view  = 'actions.registration_process',
        name  = 'actions_registration_process',
    ),
    url(
        regex = '^management/invite_process/(?P<id>\d+)/$',
        view  = 'actions.invitation_process',
        name  = 'actions_invitation_process',
    ),
    url(
        regex = '^management/email_mass_send/$',
        view  = 'actions.email_mass_send',
        name  = 'actions_email_mass_send',
    ),
    url(
        regex = '^management/synchronize/(?P<id>\d+)/$',
        view  = 'management_old.synchronize',
        name  = 'manage_synchronze',
    ),

    url(
        regex = '^management/action_process/$',
        view  = 'management_old.action_process',
        name  = 'management_action_process',
    ),

#management_action_process
    url(
        regex = '^management/reserve/(?P<id>\d+)/$',
        view  = 'management_old.reserv_add',
        name  = 'manage_reserv_add',
    ),
    url(
        regex = '^management/reserve/(?P<id>\d+)/remove/$',
        view  = 'management_old.reserve_remove',
        name  = 'manage_reserve_remove',
    ),

    # hotels
    url(
        regex = '^management/hotels/$',
        view  = 'management_old.hotel_list',
        name  = 'manage_hotel_list',
    ),
    url(
        regex = '^management/hotels/add/$',
        view  = 'management_old.hotel_add',
        name  = 'manage_hotel_add',
    ),
    url(
        regex = '^management/hotels/(?P<hotel_id>\d+)/$',
        view  = 'management_old.hotel_change',
        name  = 'manage_hotel_change',
    ),
    url(
        regex = '^management/hotels/(?P<hotel_id>\d+)/delete/$',
        view  = 'management_old.hotel_delete',
        name  = 'manage_hotel_delete',
    ),
    # rooms
    url(
        regex = '^management/hotels/rooms/(?P<room_id>\d+)/delete/$',
        view  = 'management_old.room_delete',
        name  = 'manage_room_delete',
    ),
    url(
        regex = '^management/hotels/rooms/(?P<room_id>\d+)/$',
        view  = 'management_old.room_change',
        name  = 'manage_room_change',
    ),
    url(
        regex = '^management/hotels/(?P<hotel_id>\d+)/rooms/add/$',
        view  = 'management_old.room_add',
        name  = 'manage_room_add',
    ),

)

urlpatterns += patterns('django.views.generic.simple',
    url(regex=r'^join/complete/$', view='direct_to_template',
        name='join_participant_complete', kwargs={
                'template': 'profile/join_complete.html'}),
    url(regex=r'^contact/join/complete/$', view='direct_to_template',
        name='join_contact_complete', kwargs={
                'template': 'profile/join_contact_complete.html'}),
    url(regex=r'^delegate/join/attention/$', view='direct_to_template',
        name='delegate_join_attention', kwargs={
                'template': 'profile/delegate_join_attention.html'}),
)

from profile.forms import CustomAuthenticationForm

urlpatterns += patterns('django.contrib.auth.views',
    url(regex='^login/$', view='login', name='profile_login', kwargs={
        'template_name': 'profile/login.html',
        'authentication_form': CustomAuthenticationForm}),
    url(regex='^logout/$', view='logout', name='profile_logout', kwargs={
        'next_page': '/'}),
    url(regex=r'^reset/$', view='password_reset',
        name='password_reset_form'),
    url(regex=r'^reset/done/$', view='password_reset_done'),
    url(regex=r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        view='password_reset_confirm'),
    url(r'^reset/complete/$', 'password_reset_complete'),
    url(regex=r'^change/$', view='password_change', name='password_change',),
    url(regex=r'^change/complete/$', view='password_change_done',
        name='password_change_complete'),
)

urlpatterns += patterns('profile.views.events', 
    url(r'^events/$',
        view='index', name ='events_list'),
    url(r'^(?P<id>\d+)/events/$',
        view='index', name='events_list'),
)
urlpatterns += patterns('profile.views.management.claims',
    url(r'^management/$',
        view='index', name='manage_claim_list'),
    url(r'^management/alpha/$',
        view='list_alphabetically', name='manage_claim_list_alpha'),
    url(r'^management/print/$',
        view='index', name='manage_claim_list_print', kwargs={'version': 'print'}),
    url(r'^management/badge/$',
        view='index', name='manage_claim_list_badge', kwargs={'version': 'badge'}),
    url(r'^management/(?P<id>\d+)/$',
        view='show', name='manage_claim_show'),
    url(r"^management/(?P<id>\d+)/edit/$",
        view="edit", name="claim_edit"),
    url(r'^management/(?P<id>\d+)/history/$',
        view='history', name='manage_claim_history'),
    url(r'^management/(?P<id>\d+)/payment/$',
        view='payment', name='manage_claim_payment'),
)
urlpatterns += patterns('profile.views.management.events',
    url(r'^management/events/$', view='index', name='manage_events'),
    url(r'^management/events/(?P<id>\d+)/$', view='show', name='manage_event'),
#    url(
#        regex = '^management/programm/$',
#        view  = 'management.events_programm_manager_list',
#        name  = 'events_programm_manager_list'
#    ),
#
#    #
#    url(
#        regex = '^management/events/$',
#        view  = 'management.events_list',
#        name  = 'manage_list_events',
#    ),
#    url(
#        regex = '^management/events/(?P<id>\d+)/$',
#        view  = 'management.events_change',
#        name  = 'manage_event',
#    ),
#    url(
#        regex = '^management/events/(?P<id>\d+)/print/$',
#        view  = 'management.events_change',
#        name  = 'manage_event_print',
#        kwargs = dict(printable=True),
#    ),
#    url(
#        regex = '^events/details/(?P<event_id>\d+)/$',
#        view  = 'events.ajax_event_details',
#        name  = 'ajax_event_details',
#    ),
)
