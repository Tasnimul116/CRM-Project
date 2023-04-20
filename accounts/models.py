from sre_constants import CATEGORY
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    profile_pic = models.ImageField(default='user.png',null= True,blank=True)
    
    def __str__ (self):
        return self.name or ''




class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
  
    
    def __str__ (self): return self.name




class Product(models.Model): 
    CATEGORY = (
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    
class Order(models.Model):
    STATUS=(
        ('pending', 'pending'),
        ('out for delivery', 'out for delivery'),
        ('delivered', 'delivered')
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    
    def __str__ (self):
        return self.product.name or ''
