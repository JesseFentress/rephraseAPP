from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'home.html', {'name': 'Jesse'})


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for joining!')
            return redirect('sign-up')
    else:
        form = UserCreationForm()

    return render(request, 'sign-up.html', {'form': form})
