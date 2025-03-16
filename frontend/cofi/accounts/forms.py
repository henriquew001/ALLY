from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            username_lower = username.lower()
            if CustomUser.objects.filter(username__iexact=username_lower).exists():
                raise ValidationError("A user with that username already exists (case-insensitive).")
        return username
