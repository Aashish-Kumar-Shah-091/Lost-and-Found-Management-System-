from django.urls import path
from . import views

urlpatterns = [
    path('lost/', views.lost_item_list, name='lost_item_list'),
    path('lost/create/', views.create_lost_item, name='create_lost_item'),
    path('lost/<int:pk>/', views.lost_item_detail, name='lost_item_detail'),
    path('lost/<int:pk>/delete/', views.delete_lost_item, name='delete_lost_item'),
    path('found/', views.found_item_list, name='found_item_list'),
    path('found/create/', views.create_found_item, name='create_found_item'),
    path('found/<int:pk>/', views.found_item_detail, name='found_item_detail'),
    path('found/<int:pk>/delete/', views.delete_found_item, name='delete_found_item'),
]
