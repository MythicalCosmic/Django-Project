from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewUserForm

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            if not check_exists(form.cleaned_data['username']):
                user = form.save()
                return redirect('myapp:index')
            else:
               form.add_error('username', 'This username is already taken.')
    else:
        form = NewUserForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def check_exists(username):
    return User.objects.filter(username=username).exists()
