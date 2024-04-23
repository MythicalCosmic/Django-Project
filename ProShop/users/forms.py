from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms

class NewUserForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'my-outline', 'placeholder': 'example@example.com'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'my-outline', 'placeholder': 'Enter your username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'my-outline', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'my-outline', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')