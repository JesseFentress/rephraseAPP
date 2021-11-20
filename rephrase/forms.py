from django import forms
from django.contrib.auth.forms import UserCreationForm
from rephrase.models import User, FriendsList, Chat
from django.conf.global_settings import LANGUAGES


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Username is required')
    email = forms.EmailField(max_length=30, help_text='Email is required')
    language = forms.ChoiceField(label='Select Your Language', choices=LANGUAGES, widget=forms.Select())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'language')


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=30)
    first_name = forms.CharField(label='First Name', max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
    language = forms.ChoiceField(label='Select Your Language', choices=LANGUAGES, widget=forms.Select())
    profile_img = forms.ImageField(label='Choose an Image')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'language', 'profile_img')


class AddFriendForm(forms.ModelForm):
    username = forms.CharField(label='Enter A Friends Username', max_length=30)


class CreateChatForm(forms.ModelForm):
    chat_name = forms.CharField(label='Chat Name', max_length=50)
    server = forms.IntegerField(label='Server Number')

    class Meta:
        model = Chat
        fields = ('name', 'server',)


