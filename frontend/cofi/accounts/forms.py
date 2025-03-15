from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser #only needed if you extended the User Model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser #change to User, if not using custom user model
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser #change to User, if not using custom user model
        fields = ('username', 'email')
