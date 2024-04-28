from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class ProductM(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

class OrderDetail(models.Model):
    customer_email = models.CharField(max_length=200)
    product = models.ForeignKey(ProductM, on_delete=models.PROTECT)
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200, null=True)
    has_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
