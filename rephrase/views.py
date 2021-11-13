from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from rephrase.forms import UserRegistrationForm, EditUserForm, AddFriendForm
import json
from rephrase.Graph import Graph
from rephrase.forms import UserRegistrationForm, EditUserForm
from rephrase.models import Chat, Message, User


# Create your views here.
from rephrase.models import FriendsList, User


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
    context = {}
    curr_user = request.user
    try:
        friend_list = FriendsList.objects.get(user=curr_user)
    except FriendsList.DoesNotExist:
        friend_list = FriendsList(user=curr_user)
        friend_list.save()
    if curr_user:
        friends = friend_list.friends.all()
        if friends:
            suggested_friends_dict = {User.objects.get(username=curr_user.username): []}
            for friend in friends:
                friends_friends = FriendsList.objects.get(user=friend)
                suggested_friends = friends_friends.friends.all()
                my_friend = User.objects.get(username=friend)
                if suggested_friends is not None:
                    for suggestion in suggested_friends:
                        friend_x = User.objects.get(username=suggestion)
                        if my_friend in suggested_friends_dict.keys():
                            suggested_friends_dict[my_friend].append(friend_x)
                        else:
                            suggested_friends_dict[my_friend] = [friend_x]
                        if friend_x not in suggested_friends_dict.keys():
                            suggested_friends_dict[friend_x] = []
            suggested_friends_graph = Graph(suggested_friends_dict)
            set_suggested_friends = set(suggested_friends_graph.bfs())
            set_friends = set(friends)
            set_friends.add(User.objects.get(username=curr_user))
            filtered_friends = set_suggested_friends.difference(set_friends)
            context['suggested_friends'] = filtered_friends
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


def chat(request, chat_name):
    username = 'temp_user'
    chat_details = Chat.objects.get(name=chat_name)
    
    context = {'username' : username, 'chat_details' : chat_details}
    return render(request, 'chat.html', context)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    chat_id = request.POST['chat_id']
    
    print("send view reached")
    print(message)
    print(username)
    print(chat_id)
    
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


