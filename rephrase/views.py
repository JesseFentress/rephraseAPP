from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from rephrase.forms import UserRegistrationForm, EditUserForm, AddFriendForm
import json

# Create your views here.
from rephrase.models import FriendsList, User


def home(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        context['log_form'] = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('account')
    else:
        form = AuthenticationForm()
        context['log_form'] = form
    return render(request, 'home.html', context)


def sign_up(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('account')
    else:
        form = AuthenticationForm()
        context['log_form'] = form
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def account(request):
    context = {}
    user = request.user
    users = User.objects.all()
    context['users'] = users
    try:
        friend_list = FriendsList.objects.get(user=user)
    except FriendsList.DoesNotExist:
        friend_list = FriendsList(user=user)
        friend_list.save()
    if user:
        friends = friend_list.friends.all()
        context['friends'] = friends
    if request.method == 'POST':
        friend_username = request.POST['friend_username']
        if User.objects.filter(username=friend_username):
            friend_list.add_friend(User.objects.get(username=friend_username))
            return render(request, "account.html", context)
        else:
            message = 'Username entered does not exist'
            context['error'] = message
    return render(request, "account.html", context)


def edit_account(request):
    context = {}
    user = request.user
    edit_acc_form = EditUserForm(request.POST, request.FILES, instance=user)
    if edit_acc_form.is_valid():
        edit_acc_form.save()
        return redirect('account')
    else:
        edit_acc_form = EditUserForm()
        context['edit_acc_form'] = edit_acc_form
    return render(request, 'edit.html', context)
