from django import forms
from django.contrib.auth.forms import UserCreationForm
from rephrase.models import User, FriendsList, Chat
from django.conf.global_settings import LANGUAGES
from django.utils.translation import gettext as _



class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text=_('Username is required'))
    email = forms.EmailField(max_length=30, help_text=_('Email is required'))
    language = forms.ChoiceField(label=_('Select Your Language'), choices=LANGUAGES, widget=forms.Select())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'language')


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=30)
    first_name = forms.CharField(label=_('First Name'), max_length=20)
    last_name = forms.CharField(label=_('Last Name'), max_length=20)
    language = forms.ChoiceField(label=_('Select Your Language'), choices=LANGUAGES, widget=forms.Select())
    profile_img = forms.ImageField(label=_('Choose an Image'))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'language', 'profile_img')


class CreateChatForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateChatForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = FriendsList.objects.get(user=user).friends.all()

    name = forms.CharField(label=_('Chat Name'), max_length=50)
    server = forms.IntegerField(label=_('Server Number'), required=False)
    user = forms.SelectMultiple()

    class Meta:
        model = Chat
        fields = ('name', 'server', 'user')


