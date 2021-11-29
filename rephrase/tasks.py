from celery import shared_task
import requests
from .models import Chat, User, Message


@shared_task
def translate_message(request, message):

    url = "https://google-translate20.p.rapidapi.com/translate"

    querystring = {"text": message, "tl": request.session['language'], "sl": "en"}

    headers = {
        'x-rapidapi-host': "google-translate20.p.rapidapi.com",
        'x-rapidapi-key': "1bc48f3f83msh1aab1bdcb2f9ea9p102fdfjsn5799cd77b3d7"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    text = response.json()
    return text['data']['translation']

@shared_task
def message_sessions(request):
    new_messages = []
    new_ids = []
    for chat in Chat.objects.filter(user=User.objects.get(id=request.session['_auth_user_id'])):
        if ('chat_messages_' + str(chat.id)) not in request.session.keys():
            request.session['chat_messages_' + str(chat.id)] = []
        if ('message_ids_' + str(chat.id)) not in request.session.keys():
            request.session['message_ids_' + str(chat.id)] = []
        if Message.objects.filter(chat_id=chat.id):
            for messages in Message.objects.filter(chat_id=chat.id):
                if messages.id not in request.session['message_ids_' + str(chat.id)]:
                    new_messages.append(translate_message(request, messages.text))
                    new_ids.append(messages.id)
                    request.session['chat_messages_' + str(chat.id)].append(translate_message(request, messages.text))
                    request.session['message_ids_' + str(chat.id)].append(messages.id)
                else:
                    pass