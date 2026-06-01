from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from .models import LostItem, FoundItem


def lost_item_list(request):
    items = LostItem.objects.all().order_by('-created_at')

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if q:
        items = items.filter(
            Q(item_name__icontains=q) |
            Q(description__icontains=q) |
            Q(lost_location__icontains=q)
        )
    if category:
        items = items.filter(category=category)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'items/lost_item_list.html', {
        'items': page_obj,
        'page_obj': page_obj,
        'search_query': q,
        'selected_category': category,
    })


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
        messages.success(request, 'Lost item reported successfully!')
        return redirect('lost_item_list')

    return render(request, 'items/create_lost_item.html')


def lost_item_detail(request, pk):
    item = get_object_or_404(LostItem, id=pk)
    return render(request, 'items/lost_item_detail.html', {'item': item})


@login_required
def delete_lost_item(request, pk):
    item = get_object_or_404(LostItem, id=pk)
    if item.user != request.user:
        raise Http404
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Lost item deleted successfully.')
        return redirect('lost_item_list')
    return redirect('lost_item_detail', pk=pk)


def found_item_list(request):
    items = FoundItem.objects.all().order_by('-created_at')

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if q:
        items = items.filter(
            Q(item_name__icontains=q) |
            Q(description__icontains=q) |
            Q(found_location__icontains=q)
        )
    if category:
        items = items.filter(category=category)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'items/found_item_list.html', {
        'items': page_obj,
        'page_obj': page_obj,
        'search_query': q,
        'selected_category': category,
    })


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
        messages.success(request, 'Found item reported successfully!')
        return redirect('found_item_list')

    return render(request, 'items/create_found_item.html')


def found_item_detail(request, pk):
    item = get_object_or_404(FoundItem, id=pk)
    return render(request, 'items/found_item_detail.html', {'item': item})


@login_required
def delete_found_item(request, pk):
    item = get_object_or_404(FoundItem, id=pk)
    if item.user != request.user:
        raise Http404
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Found item deleted successfully.')
        return redirect('found_item_list')
    return redirect('found_item_detail', pk=pk)
