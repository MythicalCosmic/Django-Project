from django.shortcuts import render, redirect,get_object_or_404
from .models import ProductM

def index(request):
    products = ProductM.objects.all()
    return render(request, 'index.html', {'products': products})

def indexItem(request, my_id):
    product = ProductM.objects.get(id=my_id)
    context = {
        'item': product
    }
    return render(request, 'detail.html', context=context)

def addItem(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES['upload']  
        item = ProductM(name=name, price=price, description=description, image=image)
        item.save()
        return redirect('/')  
    return render(request, 'addItem.html')
    
def update(request, my_id):
    product = get_object_or_404(ProductM, id=my_id)
    if request.method == 'POST':
        product.name = request.POST.get('name', '')
        product.price = request.POST.get('price', '')
        product.description = request.POST.get('description', '')
        if 'upload' in request.FILES:
            product.image = request.FILES['upload']  
        product.save()
        return redirect('/')
    context = {
        'item': product
    }
    return render(request, 'update.html', context=context)

def delete(request, my_id):
    product = get_object_or_404(ProductM, id=my_id)
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    context = {
        'item': product
    }
    return render(request, 'delete.html', context)
