from django.shortcuts import render, redirect
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
        return redirect('addItem')  
    return render(request, 'addItem.html')
    
def you(request):
    return render(request, 'you.html')
