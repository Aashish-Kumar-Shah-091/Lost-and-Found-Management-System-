from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import Http404

from apps.items.models import LostItem, FoundItem
from .models import Claim
from apps.claims.utils.email_service import send_lost_found_email


def claim_list(request):
    claims = Claim.objects.all().order_by('-created_at')
    return render(request, 'claims/claim_list.html', {'claims': claims})


@login_required
def create_claim(request, kind, item_id):
    model = LostItem if kind == 'lost' else FoundItem
    item = get_object_or_404(model, id=item_id)

    if request.method == 'POST':
        proof = request.POST.get('proof', '')

        ct = ContentType.objects.get_for_model(model)

        Claim.objects.create(
            claimant=request.user,
            content_type=ct,
            object_id=item.id,
            proof=proof,
        )

        if item.user.email:
            send_lost_found_email(item.user.email, item.item_name)

        messages.success(request, 'Your claim has been submitted successfully!')
        return redirect('claim_list')

    return render(request, 'claims/create_claim.html', {
        'item': item,
        'kind': kind
    })


def claim_detail(request, pk):
    claim = get_object_or_404(Claim, id=pk)

    item = None
    if claim.content_type and claim.object_id:
        model_class = claim.content_type.model_class()
        if model_class:
            item = model_class.objects.filter(id=claim.object_id).first()

    is_item_owner = item and request.user.is_authenticated and item.user == request.user

    return render(request, 'claims/claim_detail.html', {
        'claim': claim,
        'item': item,
        'is_item_owner': is_item_owner,
    })


@login_required
def approve_claim(request, pk):
    claim = get_object_or_404(Claim, id=pk)

    item = None
    if claim.content_type and claim.object_id:
        model_class = claim.content_type.model_class()
        if model_class:
            item = model_class.objects.filter(id=claim.object_id).first()

    if not item or item.user != request.user:
        raise Http404

    if request.method == 'POST':
        claim.status = 'Approved'
        claim.save()

        if hasattr(item, 'status'):
            item.status = 'Recovered' if isinstance(item, LostItem) else 'Returned'
            item.save()

        messages.success(request, f'Claim #{claim.pk} has been approved!')
        return redirect('claim_detail', pk=claim.pk)

    return redirect('claim_detail', pk=claim.pk)


@login_required
def reject_claim(request, pk):
    claim = get_object_or_404(Claim, id=pk)

    item = None
    if claim.content_type and claim.object_id:
        model_class = claim.content_type.model_class()
        if model_class:
            item = model_class.objects.filter(id=claim.object_id).first()

    if not item or item.user != request.user:
        raise Http404

    if request.method == 'POST':
        claim.status = 'Rejected'
        claim.save()
        messages.success(request, f'Claim #{claim.pk} has been rejected.')
        return redirect('claim_detail', pk=claim.pk)

    return redirect('claim_detail', pk=claim.pk)
