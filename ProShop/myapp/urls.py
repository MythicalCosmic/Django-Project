from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path("add/", views.addItem, name='addItem'),
    path("update/<int:product_id>/", views.update, name='update'),
    path('myapp/delete/<int:product_id>/', views.delete_product, name='delete'),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("failed/", views.PaymentFailedView.as_view(), name="cancel"),
    path("api/checkout-session/<int:id>/",views.create_checkout_session, name="api_checkout_session"),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
]
