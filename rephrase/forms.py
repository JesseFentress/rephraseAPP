from django import forms
from django.contrib.auth.forms import UserCreationForm
from rephrase.models import User, FriendsList, Chat, Server
from django.conf.global_settings import LANGUAGES
from django.utils.translation import gettext as _


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text=_('Username is required'))  # Username form field
    email = forms.EmailField(max_length=30, help_text=_('Email is required'))  # Email form field
    # Lanugage form field that users choices from Django Language library
    language = forms.ChoiceField(label=_('Select Your Language'), choices=LANGUAGES, widget=forms.Select())

    class Meta:
        model = User  # Corresponding model is User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'language')  # User fields


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=30)  # Email form field
    first_name = forms.CharField(label=_('First Name'), max_length=20)  # First name form field
    last_name = forms.CharField(label=_('Last Name'), max_length=20)  # Last name form field
    language = forms.ChoiceField(label=_('Select Your Language'), choices=LANGUAGES, widget=forms.Select())  # Languges
    profile_img = forms.ImageField(label=_('Choose an Image'))  # Profile image form field

    class Meta:
        model = User  # Corresponding model is USer
        fields = ('email', 'first_name', 'last_name', 'language', 'profile_img')  # Editable User fields


class CreateChatForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):  # Overrides the original __init__ function for the form
        self.user = user  # Gets the user that is dealing with the form
        super(CreateChatForm, self).__init__(*args, **kwargs)  # Inherit from the original
        self.fields['user'].queryset = FriendsList.objects.get(user=user).friends.all()  # Add the user's friends to the form
        self.fields['server'].queryset = Server.objects.all()  # Adds all servers to the form

    name = forms.CharField(label=_('Chat Name'), max_length=50)  # Chat name form field
    server = forms.Select()  # Select field for servers
    user = forms.SelectMultiple()  # SelectMultiple field to add friends to a chat

    class Meta:
        model = Chat  # Corresponding model is Chat
        fields = ('name', 'server', 'user')  # Chat fields


