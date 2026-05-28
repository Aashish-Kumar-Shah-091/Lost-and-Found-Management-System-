from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.claim_list, name='claim_list'),

    path(
        'create/<int:item_id>/',
        views.create_claim,
        name='create_claim'
    ),

    path(
        'detail/<int:pk>/',
        views.claim_detail,
        name='claim_detail'
    ),
]
