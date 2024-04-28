from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path("add/", views.addItem, name='addItem'),
    path("update/<int:my_id>/", views.update, name='update'),
    path("delete/<int:my_id>/", views.delete, name='delete'),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("failed/", views.PaymentFailedView.as_view(), name="cancel"),
    path("api/checkout-session/<int:id>/",views.create_checkout_session, name="api_checkout_session"),
]
