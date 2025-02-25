from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CreateUserForm, LoginForm

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'To create a new account, please log out first.')
        return redirect('store')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'account/register.html', context=context)


def login(request):

    if request.user.is_authenticated:
        return redirect('store')

    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)
                next_url = request.GET.get('next', request.POST.get('next'))
                return redirect(next_url or 'store')

    context = {'form': form}
    return render(request, 'account/login.html', context=context)


@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


def testview(request):
    return render(request, 'footer.html', {})
