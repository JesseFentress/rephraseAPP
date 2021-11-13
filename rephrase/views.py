from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from rephrase.forms import UserRegistrationForm, EditUserForm
from rephrase.models import Chat, Message, User


# Create your views here.
def home(request):
    return render(request, 'home.html')


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
    return render(request, "account.html")


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


def chat(request, chat_name):
    username = 'temp_user'
    chat_details = Chat.objects.get(name=chat_name)
    
    context = {'username' : username, 'chat_details' : chat_details}
    return render(request, 'chat.html', context)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    chat_id = request.POST['chat_id']
    
    new_message = Message.objects.create(text=message, user=User.objects.get(username=username), chat=Chat.objects.get(id=chat_id))
    new_message.save()
    
    return HttpResponse('Message sent successfully')

def getMessages(request, chat_name):
    chat_details = Chat.objects.get(name=chat_name)
    
    messages = Message.objects.filter(chat=chat_details)
    users = []
    for message in messages:
        users.append(User.objects.get(user=message.user_id)).username
    return JsonResponse({'messages': list(messages.values()), 'users' : users})
    

