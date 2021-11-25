from celery import shared_task
import requests


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