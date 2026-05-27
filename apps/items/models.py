from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class LostItem(models.Model):

    CATEGORY_CHOICES=[
        ('Electronics', 'Electronics'),
        ('Documents', 'Documents'),
        ('Accessories', 'Accessories'),
        ('Bags','Bags'),
        ('Others','Others')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item_name =models.CharField(max_length=100)

    category= models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    
    description = models.TextField()

    lost_location = models.CharField(max_length=200)

    lost_date = models.DateField()

    image= models.ImageField(
    upload_to ='lost_items/',
    blank =True,
    null = True
    )

    status =models.CharField(
        max_length=20,
        default='Lost'
    )

    created_at= models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.item_name
    
class FoundItem(models.Model):
    CATEGORY_CHOICES=[
        ('Electronics', 'Electronics'),
        ('Documents', 'Documents'),
        ('Accessories', 'Accessories'),
        ('Bags','Bags'),
        ('Others','Others')
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item_name=models.CharField(max_length=200)

    category=models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )   

    description = models.TextField()

    found_location = models.CharField(max_length=200)


    image=models.ImageField(
        upload_to='found_items/',
        blank=True,
        null= True
    )

    status= models.CharField(
        max_length=20,
        default='Found'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    
    )

    def __str__(self):
        return self.item_name