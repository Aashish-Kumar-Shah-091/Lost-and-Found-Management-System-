from django.shortcuts import render
from django.contrib.auth.models import User
from apps.items.models import LostItem, FoundItem


def home(request):
    context = {
        'total_lost': LostItem.objects.count(),
        'total_found': FoundItem.objects.count(),
        'recovered_items': LostItem.objects.filter(status='Recovered').count() + FoundItem.objects.filter(status='Returned').count(),
        'total_users': User.objects.count(),
        'recent_lost_items': LostItem.objects.all().order_by('-created_at')[:8],
        'recent_found_items': FoundItem.objects.all().order_by('-created_at')[:8],
    }
    return render(request, 'core/home.html', context)
