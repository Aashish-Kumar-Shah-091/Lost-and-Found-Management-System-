from django.db import models
from django.contrib.auth.models import User
from apps.items.models import item
# Create your models here.
class claim(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    ]

    claimant = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        item,
        on_delete=models.CASCADE
    )

    proof = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at= models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"{self.claimant.username} - {self.item.item_name}"