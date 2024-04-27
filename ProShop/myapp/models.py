from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='images')


    def __str__(self):
        return self.name

from django.db import models

class ProductM(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images')  

    def __str__(self):
        return self.name


