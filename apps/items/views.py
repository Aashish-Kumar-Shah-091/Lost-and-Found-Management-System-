from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LostItem, FoundItem


def lost_item_list(request):
    items = LostItem.objects.all().order_by('-created_at')
    # render modern template
    return render(request, 'items/lost_item_list_modern.html', {'object_list': items})


@login_required
def create_lost_item(request):
    if request.method == 'POST':
        item = LostItem.objects.create(
            user=request.user,
            item_name=request.POST['item_name'],
            category=request.POST['category'],
            description=request.POST['description'],
            lost_location=request.POST['lost_location'],
            lost_date=request.POST['lost_date'],
        )
        if request.FILES.get('image'):
            item.image = request.FILES['image']
            item.save()
        return redirect('lost_item_list')

    return render(request, 'items/create_lost_item.html')


def lost_item_detail(request, pk):
    item = get_object_or_404(LostItem, id=pk)
    # provide similar_items for the modern detail template
    similar = LostItem.objects.filter(category=item.category).exclude(id=item.id)[:4]
    return render(request, 'items/item_detail_modern.html', {'object': item, 'similar_items': similar})


def found_item_list(request):
    items = FoundItem.objects.all().order_by('-created_at')
    return render(request, 'items/found_item_list_modern.html', {'object_list': items})


@login_required
def create_found_item(request):
    if request.method == 'POST':
        item = FoundItem.objects.create(
            user=request.user,
            item_name=request.POST['item_name'],
            category=request.POST['category'],
            description=request.POST['description'],
            found_location=request.POST['found_location'],
        )
        if request.FILES.get('image'):
            item.image = request.FILES['image']
            item.save()
        return redirect('found_item_list')

    return render(request, 'items/create_found_item.html')


def found_item_detail(request, pk):
    item = get_object_or_404(FoundItem, id=pk)
    similar = FoundItem.objects.filter(category=item.category).exclude(id=item.id)[:4]
    return render(request, 'items/item_detail_modern.html', {'object': item, 'similar_items': similar})
