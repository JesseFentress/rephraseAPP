from celery import shared_task
import requests
from .models import Chat, User, Message


@shared_task
def translate_message(request, message):
    url = "https://google-translate20.p.rapidapi.com/translate"  # API URL
    # API query to hold message to be translated, and the language that the user wants the message to be translated to
    querystring = {"text": message, "tl": request.session['language'], "sl": "en"}
    # API call headers, including API key
    headers = {
        'x-rapidapi-host': "google-translate20.p.rapidapi.com",
        'x-rapidapi-key': "1bc48f3f83msh1aab1bdcb2f9ea9p102fdfjsn5799cd77b3d7"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)  # API response
    text = response.json()  # Grab the Json
    return text['data']['translation']  # Parse the Json response and return the translated message

@shared_task
def message_sessions(request):
    new_messages = []  # List for new messages
    new_ids = []  # List for new message ids
    for chat in Chat.objects.filter(user=User.objects.get(id=request.session['_auth_user_id'])):  # Iterate through a user's chats
        if ('chat_messages_' + str(chat.id)) not in request.session.keys():  # If a chat is not currently in the session
            request.session['chat_messages_' + str(chat.id)] = []  # Add a new session for that chat
        if ('message_ids_' + str(chat.id)) not in request.session.keys():  # If a chat's message ids is not currently in the session
            request.session['message_ids_' + str(chat.id)] = []  # Add a new session for the chat's message ids
        if Message.objects.filter(chat_id=chat.id):  # If there are messages for that current chat
            for messages in Message.objects.filter(chat_id=chat.id):  # Iterate through the messages
                if messages.id not in request.session['message_ids_' + str(chat.id)]:  # If the message is not in the session
                    new_messages.append(translate_message(request, messages.text))  # Add the translated version of that message to list
                    new_ids.append(messages.id)  # Add the messges id to list
                    request.session['chat_messages_' + str(chat.id)].append(translate_message(request, messages.text))  # Add all new messages to its corresponding session
                    request.session['message_ids_' + str(chat.id)].append(messages.id)  # Add all new message ids to its corresponding session
                else:  # If the message is in the session
                    pass   # Do nothing
