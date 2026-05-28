from django.shortcuts import render


# Create your views here.
def claim_list(request):
    return render(request, 'claims/claim_list.html')


def create_claim(request, item_id):
    context = {
        'item_id': item_id
    }

    return render(
        request,
        'claims/create_claim.html',
        context
    )


def claim_detail(request, pk):
    context = {
        'claim_id': pk
    }

    return render(
        request,
        'claims/claim_detail.html',
        context
    )