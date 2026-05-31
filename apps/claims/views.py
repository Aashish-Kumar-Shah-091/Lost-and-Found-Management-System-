from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

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

        claim = Claim.objects.create(
            claimant=request.user,
            content_type=ct,
            object_id=item.id,
            proof=proof,
        )

        if item.user.email:
            send_lost_found_email(item.user.email, item.item_name)

        return redirect('claim_list')

    return render(request, 'claims/create_claim.html', {
        'item': item,
        'kind': kind
    })


def claim_detail(request, pk):
    claim = get_object_or_404(Claim, id=pk)
    return render(request, 'claims/claim_detail.html', {'claim': claim})


def check_match(lost_item, found_item):
    if lost_item.item_name.lower() == found_item.item_name.lower():
        send_lost_found_email(
            lost_item.user.email,
            lost_item.item_name
        )
        return True
    return False
