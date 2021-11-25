from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from rephrase.forms import UserRegistrationForm, EditUserForm, CreateChatForm
from rephrase.models import Chat, Message, User, UserChat
from rephrase.Graph import Graph
from .tasks import translate_message
import requests



# Create your views here.
from rephrase.models import FriendsList, User


def home(request):
    context = {}
    user = request.user
    #del request.session['message_ids_2']
    #del request.session['message_ids_26']
    #del request.session['message_ids_1']
    #del request.session['chat_messages_2']
    #del request.session['chat_messages_26']
    #del request.session['chat_messages_1']

    if user.is_authenticated:
        request.session['language'] = request.user.language
        message_sessions(request)
        context['c'] = []
        for key, value in request.session.items():
            context['c'].append('{} => {}'.format(key, value))
    return render(request, 'home.html', context)


def message_sessions(request):
    new_messages = []
    new_ids = []
    for chat in Chat.objects.filter(user=User.objects.get(id=request.session['_auth_user_id'])):
        if ('chat_messages_' + str(chat.id)) not in request.session:
            request.session['chat_messages_' + str(chat.id)] = []
        for messages in Message.objects.filter(chat_id=chat.id):
            if ('message_ids_' + str(chat.id)) not in request.session:
                request.session['message_ids_' + str(chat.id)] = []
            if messages.id not in request.session['message_ids_' + str(chat.id)]:
                new_messages.append(translate_message(request, messages.text))
                new_ids.append(messages.id)
            else:
                pass
            l1 = list(request.session['chat_messages_' + str(chat.id)])
            request.session['chat_messages_' + str(chat.id)] = l1 + new_messages
            l2 = list(request.session['message_ids_' + str(chat.id)])
            request.session['message_ids_' + str(chat.id)] = l2 + new_ids


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


def chat_redirect(request):
    current_user = request.user
    context = {}
    userchats = list(Chat.objects.filter(user=current_user))
    if len(userchats) == 0:
        create_chat_form = CreateChatForm(request.user)
        context['create_chat_form'] = create_chat_form
        if request.method == 'POST':
            form = CreateChatForm(request.user, request.POST)
            if form.is_valid():
                form.save(commit=False)
                chat_name = form.cleaned_data['name']
                form.save()
                Chat.objects.get(name=chat_name).user.add(current_user)
            else:
                context['create_chat_form'] = create_chat_form
        return render(request, 'empty-chat.html')
    else:
        return chat(request, userchats.pop().id)


def chat_list(request):
    current_user = request.user
    userchats = Chat.objects.filter(user=current_user)
    chats = []
    for chat in list(userchats):
        chats.append(chat)
    context = {'chats': chats}
    return context


def chat(request, chat_id):
    current_user = request.user
    username = request.user.username
    chat_details = Chat.objects.get(id=chat_id)
    context = {'username' : username, 'chat_details' : chat_details}
    context.update(chat_list(request))
    create_chat_form = CreateChatForm(request.user)
    context['create_chat_form'] = create_chat_form
    if request.method == 'POST':
        form = CreateChatForm(request.user,request.POST)
        if form.is_valid():
            form.save(commit=False)
            chat_name = form.cleaned_data['name']
            form.save()
            Chat.objects.get(name=chat_name).user.add(current_user)
        else:
            context['create_chat_form'] = create_chat_form

    return render(request, 'chat.html', context)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    chat_id = request.POST['chat_id']
    if len(message.strip()) > 0:
        new_message = Message.objects.create(text=message, user=User.objects.get(username=username), chat=Chat.objects.get(id=chat_id))
        new_message.save(commit=False)
        new_id = new_message.id
        new_message.save()
        l1 = list(request.session['chat_messages_' + str(chat.id)])
        request.session['chat_messages_' + str(chat.id)] = l1 + [translate_message(request, message)]
        l2 = list(request.session['message_ids_' + str(chat.id)])
        request.session['message_ids_' + str(chat.id)] = l2 + [new_id]
    return HttpResponse('Message sent successfully')


def getMessages(request, chat_id):
    chat_details = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat_details)
    message_sessions(request)
    users = []
    date_time = []
    for message in messages:
        users.append(message.user.username)
        date_time.append(message.date_time)
        tran_msg = request.session['chat_messages_' + str(chat_id)]

    return JsonResponse({'messages': list(tran_msg), 'users': users, 'date_time': date_time})


#def translate_message(request, message):
 #   url = "https://google-translate20.p.rapidapi.com/translate"

  #  querystring = {"text": message, "tl": request.session['language'], "sl": "en"}

   # headers = {
    #    'x-rapidapi-host': "google-translate20.p.rapidapi.com",
     #   'x-rapidapi-key': "1bc48f3f83msh1aab1bdcb2f9ea9p102fdfjsn5799cd77b3d7"
    #}

    #response = requests.request("GET", url, headers=headers, params=querystring)

    #print(response.text)
    #text = response.json()
    #return text['data']['translation']
