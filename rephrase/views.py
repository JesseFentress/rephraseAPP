from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from rephrase.forms import UserRegistrationForm, UserAuthenticationForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def sign_up(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for joining!')
            user = authenticate(email=request.POST['email'], password=request.POST['password1'])
            login(request, user)
            return redirect('account')
        else:
            context['form'] = form
    else:
        form = UserRegistrationForm()
        context['form'] = form
    return render(request, 'sign-up.html', context)


def user_login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('account')
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])

            if user:
                login(request, user)
                return redirect('account')
    else:
        form = UserAuthenticationForm()
        context['log_form'] = form
    return render(request, 'login.html', context)


def account(request):
    return render(request, "account.html")