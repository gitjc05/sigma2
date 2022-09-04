from tkinter import CASCADE
from unicodedata import name
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(0)]
    )
    image = models.CharField(max_length=400)
    product_id = models.PositiveIntegerField()
    sizes = models.CharField(max_length=20)
    colors = models.CharField(max_length=400)
    
    def __str__(self):
        return self.title
    

    
    

class UserItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(default=1)
    name1 = models.CharField(max_length=200, null = True)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(0)],
        null = True
    )
    image = models.CharField(max_length=400, null=True)
    item_id = models.PositiveIntegerField(null=True)
    sizes = models.CharField(max_length=400, null=True)
    colors = models.CharField(max_length=400, null=True)
    
    def __str__(self):
        return self.product.title