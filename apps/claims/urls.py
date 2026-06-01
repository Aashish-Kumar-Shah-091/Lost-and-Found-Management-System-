from django.urls import path
from . import views

urlpatterns = [
    path('', views.claim_list, name='claim_list'),
    path('create/<str:kind>/<int:item_id>/', views.create_claim, name='create_claim'),
    path('detail/<int:pk>/', views.claim_detail, name='claim_detail'),
    path('approve/<int:pk>/', views.approve_claim, name='approve_claim'),
    path('reject/<int:pk>/', views.reject_claim, name='reject_claim'),
]
