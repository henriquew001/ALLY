from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email",) # Only the email field is needed now.

    def clean_email(self):
      email = self.cleaned_data.get("email")
      if email:
            email_lower = email.lower()
            if CustomUser.objects.filter(username__iexact=email_lower).exists():
                raise ValidationError("A user with that email already exists (case-insensitive).")
      return email
