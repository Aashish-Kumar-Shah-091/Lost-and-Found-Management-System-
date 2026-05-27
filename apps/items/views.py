from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Keep using the existing model names from migrations
from .models import LostItem, FoundItem
# Create your views here.

# LOST ITEMS

def lost_item_list(request):
    items = LostItem.objects.all().order_by('-created_at')

    return render(
        request,
        'items/lost_item_list.html',
        {'items': items}
    )


@login_required
def create_lost_item(request):
    if request.method == 'POST':
        LostItem.objects.create(
            user=request.user,
            item_name=request.POST['item_name'],
            category=request.POST['category'],
            description=request.POST['description'],
            lost_location=request.POST['lost_location'],
            lost_date=request.POST['lost_date'],
        )
        return redirect('lost_item_list')

    return render(request, 'items/create_lost_item.html')


def lost_item_detail(request, pk):
    item = get_object_or_404(LostItem, id=pk)

    return render(
        request,
        'items/lost_item_detail.html',
        {'item': item}
    )


# FOUND ITEMS


def found_item_list(request):
    items = FoundItem.objects.all().order_by('-created_at')

    return render(
        request,
        'items/found_item_list.html',
        {'items': items}
    )


@login_required
def create_found_item(request):
    if request.method == 'POST':
        FoundItem.objects.create(
            user=request.user,
            item_name=request.POST['item_name'],
            category=request.POST['category'],
            description=request.POST['description'],
            found_location=request.POST['found_location'],
            found_date=request.POST['found_date'],
        )
        return redirect('found_item_list')

    return render(request, 'items/create_found_item.html')


def found_item_detail(request, pk):
    item = get_object_or_404(FoundItem, id=pk)

    return render(
        request,
        'items/found_item_detail.html',
        {'item': item}
    )