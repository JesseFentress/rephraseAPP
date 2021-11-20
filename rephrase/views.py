from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from rephrase.forms import UserRegistrationForm, EditUserForm, CreateChatForm
from rephrase.models import Chat, Message, User, UserChat
from rephrase.Graph import Graph
import requests


# Create your views here.
from rephrase.models import FriendsList, User


def home(request):
    user = request.user
    if user.is_authenticated:
        update_session(request, user)
    return render(request, 'home.html')


def update_session(request, user):
    request.session['username'] = user.username
    suggested_friends(request, user)
   # friends = friends_list.friends.all()  # cannot pass model obj into sess, must get usernames instead
    #for friend in friends
    #request.session['friends'] = friends
    #request.session['sugg_friends'] = suggested_friends(request, user)

def suggested_friends(request, user):
    request.session['friends'] = []
    request.session['sugg_friends'] = []
    friend_list = FriendsList.objects.get(user=user)
    if user:
        friends = friend_list.friends.all()
        if friends:
            suggested_friends_dict = {User.objects.get(username=user.username): []}
            for friend in friends:
                request.session['friends'].append(friend.username)
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
            set_friends.add(User.objects.get(username=user))
            filtered_friends = set_suggested_friends.difference(set_friends)
            for fr in filtered_friends:
                request.session['sugg_friends'].append(fr.username)
        return filtered_friends

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


def chat_list(request):
    current_user = request.user
    userchats = UserChat.objects.filter(user=current_user)
    chats = []
    for userchat in userchats:
        chats.append(userchat.chat)

    context = {'chats' : chats}

    return context


def chat(request, chat_id):
    username = request.user.username
    chat_details = Chat.objects.get(id=chat_id)
    context = {'username' : username, 'chat_details' : chat_details}
    context.update(chat_list(request))
    create_chat_form = CreateChatForm()
    context['create_chat_form'] = create_chat_form
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_chat = form.save()
        else:
            context['create_chat_form'] = create_chat_form
    return render(request, 'chat.html', context)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    chat_id = request.POST['chat_id']
    new_message = Message.objects.create(text=message, user=User.objects.get(username=username), chat=Chat.objects.get(id=chat_id))
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, chat_id):
    chat_details = Chat.objects.get(id=chat_id)
    
    messages = Message.objects.filter(chat=chat_details)
    users = []
    for message in messages:

        users.append(message.user.username)

    return JsonResponse({'messages': list(messages.values()), 'users' : users})


def translate_message(chat_id):
    chat_details = Chat.objects.get(id=chat_id)

    messages = list(Message.objects.filter(chat=chat_details))
    new = []
    url = "https://google-translate20.p.rapidapi.com/translate"
    headers = {
        'x-rapidapi-host': "google-translate20.p.rapidapi.com",
        'x-rapidapi-key': "1bc48f3f83msh1aab1bdcb2f9ea9p102fdfjsn5799cd77b3d7"
    }
    for message in messages:
        new.append(requests.request("GET", url, headers=headers, params=message))

    return new

#def start_chat(request):
 #   user = request.user
  #  chats = UserChat.objects.get(user=user.username)
  #  friend_chat = 0
   # for chat in chats:
    #    if UserChat.objects.get(user=request.POST['friend_username']):
     #       friend_chat = chat.chat_id
      #      break;

   # if friend_chat == 0:
    #    user_chat = UserChat(username=user.username, chat_id=1)
     #   user_chat.save()
      #  user_chat = UserChat(username=request.POST['friend_username'], chat_id=1)
       # user_chat.save()

    #return redirect('chat')


