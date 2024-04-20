from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def indexItem(request, my_id):
    product = Product.objects.get(id=my_id)
    context = {
        'item': product
    }
    return render(request, 'detail.html', context=context)
