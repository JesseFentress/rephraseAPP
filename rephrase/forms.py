from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from rephrase.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Username is required')
    email = forms.EmailField(max_length=30, help_text='Email is required')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UserAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label='email', widget=forms.EmailInput)
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid login')
