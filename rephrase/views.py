from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from rephrase.forms import UserRegistrationForm, EditUserForm, CreateChatForm
from rephrase.models import Chat, Message, User
from rephrase.Graph import Graph
from .tasks import message_sessions




# Create your views here.
from rephrase.models import FriendsList, User


def home(request):
    context = {}  # HTML context dict
    user = request.user  # Current user
    if user.is_authenticated:  # If the user is a registered user
        request.session['language'] = request.user.language  # Grab their language code and add it to a session
        message_sessions(request)  # Add any messages they missed to their session
    return render(request, 'home.html', context)  # Render the home page


def sign_up(request):
    context = {}  # HTML context dict
    if request.method == 'POST':  # If the HTML response is a POST request
        form = UserRegistrationForm(request.POST)  # Load the form
        if form.is_valid():  # Validate the form
            user = form.save()  # Save the form and create the user
            login(request, user)  # Login the new user
            return redirect('account')  # Redirect to the account page
        else:  # If the form was not valid
            context['form'] = form  # Reload the registration form
    else:
        form = UserRegistrationForm()  # Reload the registration form
        context['form'] = form  # Add the form to the context
    return render(request, 'sign-up.html', context)  # Render the sign up page


def user_login(request):
    context = {}  # HTML context dict
    user = request.user  # Currently logged in user or anonymous user
    if user.is_authenticated:  # If the user trying to access the login page is already logged in
        return redirect('account')  # Redirect to the account page
    if request.method == 'POST':  # If the HTML response is a POST request
        form = AuthenticationForm(data=request.POST)  # Load the authentication from
        if form.is_valid():  # Validate the form
            username = form.cleaned_data.get('username')  # Grab the username
            password = form.cleaned_data.get('password')  # Grab the password
            user = authenticate(request, username=username, password=password)  # Authenticate the user to see if they exist
            if user is not None:  # If the user exists
                login(request, user)  # Login the user with build in Django login function
                return redirect('account')  # Redirect to the account page
        else:  # If the form is not valid
            form = AuthenticationForm()  # Reload the form
            context['log_form'] = form  # Add the form  to the context
            return render(request, 'login.html', context)  # Render the log in page
    else:
        form = AuthenticationForm()  # Reload the form
        context['log_form'] = form  # Add the login form to the context
    return render(request, 'login.html', context)  # Render the login page


def user_logout(request):
    logout(request)  # Log out the user with built in Django function
    return redirect('home')  # Redirect to the home page


def account(request):
    context = {}  # HTML context dict
    curr_user = request.user  # Currently logged in user
    request.session['language'] = request.user.language  # Adds the currently logged in user's language code to a session
    try:  # Check if the user has a friends list
        friend_list = FriendsList.objects.get(user=curr_user)  # Get the current user's friends list
    except FriendsList.DoesNotExist:  # If there is not friends list
        friend_list = FriendsList(user=curr_user)  # Create a friends list for the user
        friend_list.save()  # Save the friends list
    if curr_user:  # If the current user is valid
        friends = friend_list.friends.all()  # Get a queryset of all their friends
        if friends:  # If they have friends
            suggested_friends_dict = {User.objects.get(username=curr_user.username): []}  # Create a dictionary to form a graph
            for friend in friends:  # Iterate through all of the user's friends
                friends_friends = FriendsList.objects.get(user=friend)  # Get the friend's friends list
                suggested_friends = friends_friends.friends.all()  # Queryset of all their friends
                my_friend = User.objects.get(username=friend)  # Get the User object related to the friend
                if suggested_friends is not None:  # If the friend as friends
                    for suggestion in suggested_friends:  # Iterate through their friends
                        friend_x = User.objects.get(username=suggestion)  # Get the User object related to the friend's friend
                        if my_friend in suggested_friends_dict.keys():  # If the User's friend does have a dict key yet
                            suggested_friends_dict[my_friend].append(friend_x)  # Add the friends friend to the list
                        else:  # If there is not a dict key, or vertex, for the friend
                            suggested_friends_dict[my_friend] = [friend_x]  # Create a new key of the friend (edge) with their friend as a value (edge)
                        if friend_x not in suggested_friends_dict.keys():  # If the friend's friend is not a vertex yet add them as a key
                            suggested_friends_dict[friend_x] = []  # Create new vertex for the friend's friend
            suggested_friends_graph = Graph(suggested_friends_dict)  # Creates a graph with the dictionary of friends
            set_suggested_friends = set(suggested_friends_graph.bfs())  # Creates a set of the suggested friends
            set_friends = set(friends)  # Turns the list of user's friends into a set
            set_friends.add(User.objects.get(username=curr_user))  # Adds the current user to the friend's set
            filtered_friends = set_suggested_friends.difference(set_friends)  # Get the difference of the two sets
            context['suggested_friends'] = filtered_friends  # Adds the new set of suggested friends to the context
            context['friends'] = friends  # Adds user's friends list to the context
    if request.method == 'POST':  # If the HTML response is a POST request
        friend_username = request.POST['friend_username']  # Get the username data from the POST request
        if User.objects.filter(username=friend_username):  # Find the User object related to the username
            friend_list.add_friend(User.objects.get(username=friend_username))  # Add the related User to the current user's friends list
            return redirect('account')  # Redirect to load changes
        else:
            message = 'Username entered does not exist'  # If the user entered an invalid username
            context['error'] = message  # Add error message to the context
    return render(request, "account.html", context)  # Render the account page


def edit_account(request):
    context = {}  # Html context dict
    user = request.user  # Currently logged in user
    edit_acc_form = EditUserForm(request.POST, request.FILES, instance=user)  # Load edit account form
    if edit_acc_form.is_valid():  # Validates the form
        edit_acc_form.save()  # Save the form and change the users information
        request.session['language'] = request.user.language  # If the language got changed save it to the session
        return redirect('account')  # Redirect to the account page
    else:
        edit_acc_form = EditUserForm()  # If the form was not valid reload the form
        context['edit_acc_form'] = edit_acc_form  # Add the form back to the context
    return render(request, 'edit.html', context)  # Loads the edit account page


def chat_redirect(request):
    current_user = request.user  # Currently logged in user
    context = {}  # HTML context dict
    userchats = list(Chat.objects.filter(user=current_user))  # List of chat objects the user belongs to
    create_chat_form = CreateChatForm(request.user, request.POST)  # Load chat creation form
    context['create_chat_form'] = create_chat_form  # Adds chat creation form to the context
    if len(userchats) == 0:  # As long as a user belongs to chats
        if request.method == 'POST':  # If the HTML response is a POST request
            form = CreateChatForm(request.user, request.POST)  # Load the form with user and POST data
            if form.is_valid():  # Validates the form
                form.save(commit=False)  # Pause saving the form
                chat_name = form.cleaned_data['name']  # Grab the name of the chat
                form.save()  # Save the form and create the new chat
                Chat.objects.get(name=chat_name).user.add(current_user)  # Add the current user to the chat that was just created
                return redirect('chat', Chat.objects.get(name=chat_name).id)  # Redirect to the newly created chat
            else:
                context['create_chat_form'] = create_chat_form  # If the from was not valid reload it into the context
        return render(request, 'empty-chat.html', context)  # Render the html page for users with no chats
    else:
        return chat(request, userchats.pop().id)  # Redirect using the chat function with the most recently created chat


def chat_list(request):
    current_user = request.user  # Currently logged in user
    userchats = Chat.objects.filter(user=current_user)  # Queryset of chat objects that the user belongs to
    chats = []  # Empty list of chats
    for chat in list(userchats): # For every chat object in the queryset cast as a list
        chats.append(chat)  # Add the chat to the chats list
    context = {'chats': chats}  # Add the list to the HTML context dict
    return context  # Return the context dict


def chat(request, chat_id):
    current_user = request.user  # Currently logged in user
    username = request.user.username  # User's username
    chat_details = Chat.objects.get(id=chat_id)  # Get the chat object related to particular chat
    context = {'username': username, 'chat_details': chat_details}  # HTML context dict to hold user and chat data
    context.update(chat_list(request))  # Updates the list of chats that the user belongs to
    create_chat_form = CreateChatForm(request.user)  # Load chat creation form
    context['create_chat_form'] = create_chat_form  # Adds the form to the HTML context dict
    if request.method == 'POST':  # If the HTML response is a POST request
        form = CreateChatForm(request.user, request.POST)  # Load the form again with the POST and user data
        if form.is_valid():  # Validates the form
            form.save(commit=False)  # Pause saving the form
            chat_name = form.cleaned_data['name']  # Grab the chat name from the form
            form.save()  # Save the form and create a new chat
            Chat.objects.get(name=chat_name).user.add(current_user)  # Add the current user to the chat that was just created
            return redirect('chat', chat_id)  # Redirect back to the current page to load changes to the chat list
        else:
            context['create_chat_form'] = create_chat_form  # If the form was invalid reload it back into the context
    return render(request, 'chat.html', context)  # Render the html page with the context


def send(request):
    message = request.POST['message']  # Gets message content of HTTP POST response
    username = request.POST['username']  # Gets username content of HTTP POST response
    chat_id = request.POST['chat_id']  # Gets chat_id content of HTTP POST response
    if len(message.strip()) > 0:  # Verify if the message is an empty message or not
        new_message = Message.objects.create(text=message, user=User.objects.get(username=username), chat=Chat.objects.get(id=chat_id))
        new_message.save()  # Create a new message object with the POST data
    return HttpResponse('Message sent successfully')  # Return an HTTP response


def getMessages(request, chat_id):
    chat_details = Chat.objects.get(id=chat_id)  # Get the chat object related to the particular chat
    messages = Message.objects.filter(chat=chat_details)  # Get a queryset of messages that belong to chat
    if len(list(messages)) > 0:  # If there are messages belonging to the chat
        message_sessions(request)  # Use message_sessions to translate and load messages into the user's session
        users = []  # Holds message senders
        date_time = []  # Holds date and time message was sent
        for message in messages:  # Iterate through the current chats messages
            users.append(message.user.username)  # Add the sender of a message to the list
            date_time.append(message.date_time)  # Add when the message was sent to the list
            tran_msg = request.session['chat_messages_' + str(chat_id)]  # tran_msg is set to the cht messages session for this user corresponding to this chat
        return JsonResponse({'messages': list(tran_msg), 'users': users, 'date_time': date_time})  # Return a JSON response with the lists
    else:
        return JsonResponse({'messages': [], 'users': [], 'date_time': []})  # If the chat is empty return an empty response


def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })