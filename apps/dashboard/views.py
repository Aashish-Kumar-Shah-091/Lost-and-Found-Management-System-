from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.items.models import LostItem, FoundItem
from apps.claims.models import Claim


@login_required
def dashboard(request):
    user = request.user
    user_lost = LostItem.objects.filter(user=user).order_by('-created_at')
    user_found = FoundItem.objects.filter(user=user).order_by('-created_at')
    user_claims = Claim.objects.filter(claimant=user).order_by('-created_at')

    context = {
        'user_lost_count': user_lost.count(),
        'user_found_count': user_found.count(),
        'matches_count': user_claims.filter(status='Approved').count(),
        'notifications_count': user_claims.filter(status='Pending').count(),
        'recent_lost': user_lost[:5],
        'recent_found': user_found[:5],
        'recent_claims': user_claims[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)
