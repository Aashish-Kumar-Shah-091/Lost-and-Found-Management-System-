from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from apps.items.models import LostItem, FoundItem
from apps.claims.models import Claim
from .forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    lost_items = LostItem.objects.filter(user=user).order_by('-created_at')
    found_items = FoundItem.objects.filter(user=user).order_by('-created_at')

    from itertools import chain
    recent_items = sorted(
        chain(lost_items[:3], found_items[:3]),
        key=lambda x: x.created_at,
        reverse=True
    )[:5]

    context = {
        'user_lost_count': lost_items.count(),
        'user_found_count': found_items.count(),
        'user_claims_count': Claim.objects.filter(claimant=user).count(),
        'recent_items': recent_items,
    }
    return render(request, 'accounts/profile.html', context)
