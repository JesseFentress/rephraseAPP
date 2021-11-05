from django import forms
from django.contrib.auth.forms import UserCreationForm
from rephrase.models import User, Profile
from rephraseAPP.settings import LANGUAGE_CHOICES


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Username is required')
    email = forms.EmailField(max_length=30, help_text='Email is required')
    language = forms.ChoiceField(label='Select Your Language', choices=LANGUAGE_CHOICES, widget=forms.Select())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'language')


class UserProfileForm(forms.ModelForm):
    language = forms.ChoiceField(label='Select Your Language', choices=LANGUAGE_CHOICES, widget=forms.Select())

    class Meta:
        model = Profile
        fields = ('language',)


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=30)
    first_name = forms.CharField(label='First Name', max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
    language = forms.ChoiceField(label='Select Your Language', choices=LANGUAGE_CHOICES, widget=forms.Select())
    profile_img = forms.ImageField(label='Choose an Image')

    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'language', 'profile_img')

