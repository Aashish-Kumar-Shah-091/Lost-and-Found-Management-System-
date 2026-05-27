# Register your models here.
from django.contrib import admin
from .models import LostItem, FoundItem

# Register your models here.
admin.site.register(LostItem)
admin.site.register(FoundItem)