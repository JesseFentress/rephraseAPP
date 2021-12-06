# rephraseAPP
translation application
This application can be found on Heroku at: https://app-rephrase.herokuapp.com/
* Create an account *
* Add users Jesse, or bew5294, and create a chat to test the code*

#####################
Dependencies include: 
celery==5.2.1
Django==3.2.9
gunicorn==20.1.0
Pillow==8.4.0
psycopg2-binary==2.9.2
requests==2.22.0

* psycopg2-binary and gunicorn are dependecy that are required to host the app on Heroku and are not need to run the code locally. *
* gunicorn requires a Linux system to run *

#####################
If running locally,  "python manage.py makemigrations" and "python manage.py migrate in the project directory to configure the database, then "python manage.py runserver" to run
the application locally. There will be no data as the application will be running on a local database, therefore, new users/chats/messages will need to be created to test the code.
