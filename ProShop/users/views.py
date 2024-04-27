from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import NewUserForm
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            if not check_exists(form.cleaned_data['username']):
                user = form.save()
                login(request, user)
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

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
@login_required
def profile(request):
    return render(request, 'profile.html')


def seller(request, id):
    seller = User.objects.get(id=id)
    context = {'seller': seller}
    return render(request, 'seller.html', context=context)