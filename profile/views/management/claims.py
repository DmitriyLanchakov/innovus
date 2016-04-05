# encoding: utf-8
from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from openteam.utils import send_email
from profile import filters
from profile.forms import ActionForm, ClaimsFilterForm, EmailMessageForm, StateForm, ClaimForm, PaymentForm
from profile import settings as profile_settings
from profile.models import Claim, History
from profile.utils import get_filtered_claims
from profile.views.actions import RequestAdditionalInfo, ParticipantRegistration, ParticipantInvitation

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to()
def index(request, version=False):
    action_form  = ActionForm(initial={ 'action_code': profile_settings.ACTION_RESEND_ACTIVATION })
    filter_form  = ClaimsFilterForm(request.POST or None)
    message_form = EmailMessageForm()

    if filter_form.is_valid():
        data = filter_form.cleaned_data
        request.session['filter_data'] = data
        request.session.save()

    else:
        data = request.session.get('filter_data', dict())
        filter_form = ClaimsFilterForm(initial=data)

    claims, filter_set = get_filtered_claims(data)

    order_format = "?of=%d&ot=%s"
    list_order = ['last_name', 'creation_date']
    ordering = [order_format % (i, 'asc') for i in xrange(len(list_order))]

    if request.GET.get('ot', None) and request.GET.get('of', None):
        order_field = int(request.GET['of'])
        order_string = list_order[order_field]
        if request.GET['ot'] == "desc":
            order_string = '-' + order_string
        claims = claims.order_by(order_string)
        ordering[order_field] = order_format % (order_field, 'desc' if request.GET['ot'] == 'asc' else 'asc')

    return {
        'TEMPLATE': 'admin/claims/list%s.html' % ('_' + version if version else ''),
        'claims': claims,
        'filter_form': filter_form,
        'action_form': action_form,
        'message_form': message_form,
        'manage_claim': True,
        'filter_set': filter_set,
        'ordering': ordering,
    }

@render_to('admin/claims/list_print_alpha.html')
@login_required
@user_passes_test(lambda u: u.is_staff)
def list_alphabetically(request):
    russians_by_letter = list()
    useless_states = [profile_settings.CLAIM_REJECTED, profile_settings.CLAIM_CANCELLED]

    claims_cleaned = Claim.objects.exclude(claim_state__in=useless_states)
    foreigners = claims_cleaned.exclude(country__pk=profile_settings.RUSSIA_COUNTRY_ID).order_by('last_name', 'first_name', 'middle_name')
    russians = claims_cleaned.filter(country__pk=profile_settings.RUSSIA_COUNTRY_ID)

    alphabet = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
    for letter in alphabet:
        russians_by_letter.append(( unicode(letter), russians.filter(last_name__startswith = letter).order_by('last_name', 'first_name', 'middle_name') ))

    return {'foreigners': foreigners, 'russians': russians_by_letter}


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/show.html')
def show(request, id):
    claim = get_object_or_404(Claim, id=id)

    actions = list()
    for state_code in claim.next_states:
        title = filters.CLAIM_STATES_ACTIONS[state_code]
        actions.append( (title, StateForm(initial={'new_state': state_code})) )

    request_action = RequestAdditionalInfo(claim).get_action_form()

    return dict(
        claim = claim,
        actions = actions,
        request_action = request_action,
        action_form = ActionForm(initial={ 'action_code': profile_settings.ACTION_RESEND_RESERVATION }),
        registration_form = ParticipantRegistration(claim).get_action_form(),
        invitation_form = ParticipantInvitation(claim).get_action_form()
    )

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/claim_edit.html')
def edit(request, id):
    claim = get_object_or_404(Claim, pk=id)
    form = ClaimForm(request.POST or None, instance=claim)
    if form.is_valid():
        claim = form.save()
        if claim.user:
            claim.user.username = request.POST['email']
            claim.email = request.POST['email']
            claim.user.save()
            claim.save()
        return redirect('manage_claim_show', id=claim.pk)
    vt = _('Delegation management')
    return {'delegate': claim, 'claim_form': form, 'view_title': vt, 'is_delegate_list': True}

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/claim_history.html')
def history(request, id):
    claim = get_object_or_404(Claim, pk=id)
    return {'changes': History.objects.filter(claim=claim).order_by('timestamp')}

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/claim_payment.html')
def payment(request, id):
    claim = get_object_or_404(Claim, pk=id)
    if not (claim.is_waiting_payment() or claim.payment_date):
        raise Http404('This claim isn\'t waiting for payment')

    form = PaymentForm(request.POST or None, initial={
                'sum': claim.payment_sum,
                'date': claim.payment_date})
    if form.is_valid():
        claim.payment(
            form.cleaned_data['sum'],
            form.cleaned_data['date'],
        )
        # force update
        claim = Claim.objects.get(id=claim.id)

        send_email(claim.get_email, 'payment', dict(claim=claim))
        return redirect('manage_claim_show', id=claim.pk)

    sum = 1000 * int(settings.COST2_NUMERIC if claim.creation_date >= settings.DATE_X else settings.COST1_NUMERIC)
    return {'claim': claim, 'form': form, 'sum': sum}
