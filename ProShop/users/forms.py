from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class NewUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'my-outline', 'placeholder': 'example@example.com'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'my-outline', 'placeholder': 'Enter your username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'my-outline', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'my-outline', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2') 
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def checkExists(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            return True
        else:
            return False
        


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Invalid username or password. Please try again.",
        'inactive': "This account is inactive.",
    }
