from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from apps.items.models import LostItem, FoundItem
from .models import Claim


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
        return redirect('claim_list')

    return render(request, 'claims/create_claim.html', {'item': item, 'kind': kind})


def claim_detail(request, pk):
    claim = get_object_or_404(Claim, id=pk)
    return render(request, 'claims/claim_detail.html', {'claim': claim})
