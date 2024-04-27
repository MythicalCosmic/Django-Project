from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('sellerProfile/<int:id>/', views.seller, name='seller'),

]
 