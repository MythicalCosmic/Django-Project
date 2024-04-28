from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductM, OrderDetail
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView
from django.core.paginator import Paginator 
from django.urls import reverse
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging
from django.db.models import ProtectedError
from .models import Product, Review
from .forms import ReviewForm
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from django.contrib import messages


@login_required
def index(request):
    all_products = ProductM.objects.all()
    items_per_page = 3
    item_name = request.GET.get('search', '') 
    
    if item_name:
        page_obj = all_products.filter(name__icontains=item_name)
    else:
        page_obj = all_products
    
    paginator = Paginator(page_obj, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    current_path = reverse('myapp:index')
    previous_page_url = None
    next_page_url = None
    
    if page_obj.has_previous():
        previous_page_url = f"{current_path}?page={page_obj.previous_page_number()}"
    if page_obj.has_next():
        next_page_url = f"{current_path}?page={page_obj.next_page_number()}"
    
    first_page_url = current_path
    last_page_url = f"{current_path}?page={paginator.num_pages}"
    
    return render(request, 'index.html', {
        'products': page_obj, 
        'first_page_url': first_page_url,
        'previous_page_url': previous_page_url, 
        'next_page_url': next_page_url,
        'last_page_url': last_page_url, 
        'current_path': current_path
    })

@login_required
def addItem(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('upload')  
        seller = request.user
        item = ProductM.objects.create(name=name, price=price, description=description, image=image, seller=seller)
        return redirect('myapp:index')
    return render(request, 'addItem.html')

@login_required   
def update(request, product_id):
    product = get_object_or_404(ProductM, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name', '')
        product.price = request.POST.get('price', '')
        product.description = request.POST.get('description', '')
        if 'upload' in request.FILES:
            product.image = request.FILES['upload']  
        product.save()
        return redirect('myapp:index')
    context = {'item': product}
    return render(request, 'update.html', context=context)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(ProductM, pk=product_id)
    if request.method == 'POST':
        try:
            product.delete()
            return redirect('myapp:index')
        except ProtectedError as e:
            error_message = "Cannot delete the product because it is referenced by OrderDetail objects."
            return HttpResponse(error_message, status=400)  
    return render(request, 'delete.html', {'product': product})

class ProductDetailView(DetailView):
    model = ProductM
    template_name = 'detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context
    
@login_required
@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(ProductM, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("myapp:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("myapp:cancel")),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = OrderDetail()
    order.product = product
    order.stripe_payment_intent = checkout_session["payment_intent"]
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({"sessionId": checkout_session.id})



logger = logging.getLogger(__name__)

class PaymentSuccessView(TemplateView):
    template_name = "success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()

        logger.info("Session ID: %s", session_id)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        logger.info("Payment Intent: %s", session.payment_intent)  

        try:
            order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
            order.has_paid = True
            order.save()
        except Exception as e:
            # Log the error
            logger.error(f"Error occurred while saving order: {e}")

        return render(request, 'success.html')
    


class PaymentFailedView(TemplateView):
    template_name = 'fail.html'



def product_detail_view(request, product_id):
    product = get_object_or_404(ProductM, pk=product_id)
    reviews = Review.objects.filter(product=product)  
    return render(request, 'detail.html', {'product': product, 'reviews': reviews})


@login_required
def add_review(request, product_id):
    product = ProductM.objects.get(id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('myapp:detail', pk=product_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})