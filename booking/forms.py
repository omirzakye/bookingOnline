from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django import forms


class CustomRegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'name':"first_name", 'type':"first name", 'placeholder':"First Name"}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'name':"last_name", 'type':"last name", 'placeholder':"Last Name"}))
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': "username", 'type': "username", 'placeholder': "Username"}))
    email_address = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': "email_address", 'type': "email address", 'placeholder': "Email Address"}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'name':"password1", 'type':"password", 'placeholder':"Password"}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'name':"password2", 'type':"password", 'placeholder':"Confirm Password"}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email_address', 'password1', 'password2')


class CustomLoginUserForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'name': "username", 'type': "username", 'placeholder': "Username"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': "password", 'type': "password", 'placeholder': "Password"}))
